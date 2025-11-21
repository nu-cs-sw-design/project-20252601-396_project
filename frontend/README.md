# Fast Food Ordering System - Frontend

React TypeScript frontend for the Fast Food Ordering System.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

The app will open at `http://localhost:3000` in your browser.

## Project Structure

- `src/`
  - `components/` - React components
  - `services/` - API service layer
    - `api.ts` - API client and endpoints
  - `types/` - TypeScript type definitions
  - `utils/` - Utility functions
  - `App.tsx` - Main application component

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner

## API Configuration

The frontend is configured to proxy API requests to `http://localhost:5000` (Flask backend). This is configured in `package.json` with the `proxy` field.

For production, update the `REACT_APP_API_URL` environment variable to point to your backend API.
