# TSV-RSM Frontend - Local Development Setup Guide

This guide will help you set up and run the TSV-RSM frontend application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 18+ LTS
  - Check version: `node --version`
  - Download from: https://nodejs.org/

- **npm**: Comes with Node.js
  - Check version: `npm --version`

- **Backend API**: The backend must be running on `http://localhost:8000`
  - See `backend/README.md` for backend setup instructions

## Installation Steps

### 1. Navigate to Frontend Directory

```bash
cd ~/Documents/programming/python/devin_rsm/frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages including:
- React 18
- TypeScript
- Vite (build tool)
- TanStack Query (data fetching)
- React Router (routing)
- Tailwind CSS (styling)
- Zod (validation)
- Generated OpenAPI SDK

### 3. Configure Environment Variables

Create a `.env` file in the frontend directory:

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

**Important**: Make sure this URL matches your running backend server.

## Running the Development Server

### Start the Frontend

```bash
npm run dev
```

The application will start on **http://localhost:5173**

You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should see the login page with the TSV logo.

## Testing the Application

### 1. Ensure Backend is Running

Before testing the frontend, make sure your backend is running:

```bash
# In a separate terminal
cd ~/Documents/programming/python/devin_rsm/backend
poetry run uvicorn app.main:app --reload
```

Backend should be accessible at: http://localhost:8000

### 2. Create a Test User (if not already done)

```bash
cd ~/Documents/programming/python/devin_rsm/backend
poetry run python -m scripts.create_test_user
```

This will create a test user in your database. The script will display the credentials after creation.

### 3. Test Login Flow

1. Navigate to http://localhost:5173
2. Enter the test credentials created by the script above
3. Click "Sign in"
4. You should be redirected to the dashboard

### 4. Open Browser DevTools

Press `F12` or `Cmd+Option+I` (Mac) to open browser developer tools:

- **Console tab**: Check for any JavaScript errors
- **Network tab**: Monitor API requests to http://localhost:8000
- **Application tab**: View stored tokens in LocalStorage

## Project Structure

```
frontend/
├── public/                 # Static assets
│   └── logo.png           # TSV logo
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── DashboardLayout.tsx
│   │   └── ProtectedRoute.tsx
│   ├── contexts/          # React contexts
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   ├── lib/               # Utilities and SDK
│   │   ├── apiClient.ts   # API client wrapper
│   │   └── sdk/           # Generated TypeScript SDK
│   ├── pages/             # Page components
│   │   ├── LoginPage.tsx
│   │   └── DashboardPage.tsx
│   ├── styles/            # Global styles
│   │   └── index.css
│   ├── types/             # TypeScript types
│   │   └── auth.ts
│   ├── main.tsx           # Entry point
│   └── vite-env.d.ts      # Vite type definitions
├── .env                   # Environment variables (create this)
├── .env.example           # Example environment file
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── vite.config.ts         # Vite config
└── tailwind.config.js     # Tailwind CSS config
```

## Available Scripts

### Development

```bash
npm run dev
```
Starts the development server with hot reload on http://localhost:5173

### Build for Production

```bash
npm run build
```
Creates optimized production build in `dist/` directory

### Preview Production Build

```bash
npm run preview
```
Preview the production build locally

### Linting

```bash
npm run lint
```
Check code for linting errors

```bash
npm run lint --fix
```
Fix auto-fixable linting errors

### Type Checking

TypeScript is checked automatically during development, but you can also run:
```bash
npx tsc --noEmit
```

### Regenerate SDK

If backend API changes, regenerate the TypeScript SDK:
```bash
npm run generate:sdk
```

This will:
1. Export OpenAPI spec from backend
2. Generate new TypeScript types and services in `src/lib/sdk/`

## Authentication Flow

### How It Works

1. **Login**: User enters credentials → API returns access token + refresh token
2. **Storage**: Tokens stored in browser's LocalStorage
3. **API Calls**: Access token automatically added to all API requests
4. **Token Refresh**: When access token expires (15 min), refresh token used to get new one
5. **Logout**: Tokens removed from storage and revoked on backend

### Stored Data

Check LocalStorage in browser DevTools (Application tab):
- `access_token`: JWT for API authentication (expires in 15 min)
- `refresh_token`: JWT for getting new access tokens (expires in 7 days)

### API Integration

The frontend uses the generated TypeScript SDK from `src/lib/sdk/`:

```typescript
import { ApiClient } from '@/lib/apiClient';

// Login
const response = await ApiClient.auth.login({ email, password });

// Get current user
const user = await ApiClient.auth.getMe();

// List companies
const companies = await ApiClient.companies.listCompanies();

// List stores
const stores = await ApiClient.stores.listStores();
```

## Common Issues

### Issue: "Failed to fetch" or Network Error

**Solution**: Ensure backend is running on http://localhost:8000
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

### Issue: CORS Error

**Solution**: The backend already has CORS configured for http://localhost:5173. If you see CORS errors:
1. Check backend logs for errors
2. Verify CORS settings in `backend/app/main.py`
3. Ensure you're accessing frontend at http://localhost:5173 (not 127.0.0.1)

### Issue: "Module not found" Errors

**Solution**: Reinstall dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: Port 5173 Already in Use

**Solution**: Kill the process using port 5173
```bash
# Find process
lsof -i :5173

# Kill it (replace PID with actual process ID)
kill -9 <PID>

# Or use a different port
npm run dev -- --port 3000
```

### Issue: Dark Mode Not Working

**Solution**: The theme is stored in LocalStorage. Clear it:
```javascript
// In browser console
localStorage.removeItem('theme')
location.reload()
```

### Issue: Login Redirects to 404

**Solution**: Check React Router configuration in `src/main.tsx`. Ensure routes are defined:
- `/` → Login page
- `/dashboard` → Dashboard page (protected)

## Development Workflow

### Making Changes

1. **Edit files**: Changes auto-reload in browser (hot module replacement)
2. **Check console**: Monitor for errors in browser DevTools
3. **Test**: Verify changes work correctly
4. **Commit**: When satisfied with changes

### Adding New Pages

1. Create page component in `src/pages/`
2. Add route in `src/main.tsx`
3. Add navigation link in `src/components/DashboardLayout.tsx` (if needed)
4. Add authentication protection with `<ProtectedRoute>` if needed

### Adding New API Calls

1. Check if SDK needs regeneration: `npm run generate:sdk`
2. Use `ApiClient` from `src/lib/apiClient.ts`
3. Types are automatically available from SDK

### Styling

- Use Tailwind CSS utility classes
- Use `dark:` prefix for dark mode styles
- Example: `className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white"`

## Testing Credentials

For local testing, create a test user using:
```bash
cd backend
poetry run python -m scripts.create_test_user
```

The script will display the test credentials after creating the user.

## Next Steps

After successful login, you should:
1. See the dashboard with welcome message
2. Be able to navigate using the sidebar
3. Test logout functionality
4. Explore company and store management (once implemented)

## Need Help?

- **Backend not working?** See `backend/README.md`
- **Database issues?** Check backend database connection
- **Authentication failing?** Verify test user exists in database
- **Frontend crashes?** Check browser console for errors

## Architecture Notes

### State Management
- **Auth State**: Managed by `AuthContext`
- **Theme State**: Managed by `ThemeContext`
- **Server State**: TanStack Query (for future API data caching)

### Type Safety
- Full TypeScript coverage
- Generated types from OpenAPI spec
- Zod validation for forms

### Styling
- Tailwind CSS for utility-first styling
- Custom components in `src/components/`
- Dark mode support with system preference detection

### API Client
- Auto-generated from OpenAPI spec
- Type-safe requests and responses
- Automatic token management
- Centralized error handling

---

**Happy coding! 🚀**

For any issues or questions, check the main project documentation in `Docs/` directory.
