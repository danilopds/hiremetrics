# HireMetrics Frontend

This is the frontend application for HireMetrics, a comprehensive SaaS platform for Brazilian HR professionals and recruiters to analyze job market trends, company insights, and talent demand using real-time data visualization and advanced analytics.

## Tech Stack

- **Vue 3** - Modern reactive framework with Composition API
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **ECharts** - Data visualization
- **MapLibre GL JS** - Geographic data visualization
- **Tailwind CSS** - Utility-first CSS framework
- **Naive UI** - Vue 3 component library
- **Vite** - Fast build tool

## Project Structure

```
frontend/
├── docs/               # Documentation
│   └── STYLE_GUIDE.md  # Coding and styling standards
├── public/             # Static assets served as-is
├── src/
│   ├── api/            # API integration
│   │   ├── config.js   # Centralized API configuration
│   │   └── ...         # API modules by feature
│   ├── assets/         # Assets that will be processed by build tools
│   │   ├── img/        # Images
│   │   └── tailwind.css # Main CSS file
│   ├── components/     # Reusable Vue components
│   │   ├── charts/     # Chart components
│   │   ├── common/     # Common UI components
│   │   ├── filters/    # Filter components
│   │   └── maps/       # Map components
│   ├── router/         # Vue Router configuration
│   ├── stores/         # Pinia stores
│   ├── styles/         # Global styles and tokens
│   │   └── tokens.js   # Design tokens
│   ├── utils/          # Utility functions
│   │   └── chartConfig.js # Chart configuration utilities
│   ├── views/          # Page components
│   ├── App.vue         # Root component
│   └── main.js         # Application entry point
├── index.html          # HTML template
├── package.json        # Dependencies and scripts
├── tailwind.config.js  # Tailwind CSS configuration
└── vite.config.js      # Vite configuration
```

## Getting Started

### Prerequisites

- Node.js (v16+)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Code Standards

We follow a set of coding standards to maintain consistency across the codebase. Please refer to the [Style Guide](./docs/STYLE_GUIDE.md) for detailed information.

### Key Principles

1. **Component Structure**
   - Use Vue 3 Composition API with `<script setup>`
   - Follow consistent component organization

2. **Styling**
   - Use Tailwind CSS utilities for styling
   - Follow the color system defined in `src/styles/tokens.js`

3. **State Management**
   - Use Pinia stores for global state
   - Follow consistent store patterns

4. **API Integration**
   - Use centralized API configuration from `src/api/config.js`
   - Handle errors consistently

5. **Charts and Data Visualization**
   - Use standardized chart configurations from `src/utils/chartConfig.js`
   - Maintain consistent styling across all charts

## Contributing

1. Follow the code standards in the [Style Guide](./docs/STYLE_GUIDE.md)
2. Use consistent naming conventions
3. Write clear, descriptive commit messages
4. Add appropriate documentation
5. Test your changes thoroughly

## License

[MIT](../LICENSE)
