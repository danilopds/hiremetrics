with stg_jobs as (
    SELECT *, ROW_NUMBER() OVER ( partition by employer_name ) name_row
    from {{ ref('stg_jobs') }}
),

employer_dedup as (
  select * from
  (
    -- step 2: dedup by name
    SELECT 
      FIRST_VALUE(employer_name) OVER (PARTITION BY lower(employer_name_dedup1) ORDER BY employer_name) as employer_name_dedup2,
      *
    FROM
    (
    -- step 1: dedup by website
    SELECT 
      FIRST_VALUE(employer_name) OVER (PARTITION BY lower(calculated_employer_website) ORDER BY employer_name) as employer_name_dedup1,
      *
      from (
      -- step 0: not-null employer_name  
        select
        case
            when employer_website is null then employer_name
            else employer_website
        end as calculated_employer_website,
        *,
        FROM stg_jobs
      )
    )
  )
)

select
    {{ dbt_utils.generate_surrogate_key(['employer_dedup.employer_name']) }} as employer_key,
    employer_dedup.employer_name_dedup2 as employer_name,
    employer_dedup.employer_logo,
    employer_dedup.employer_website,
    --audit columns
    employer_dedup.created_at,
    now() AS updated_at,
    employer_dedup.created_by,
    'dim_employer_transform' AS updated_by
from employer_dedup
where employer_dedup.name_row = 1