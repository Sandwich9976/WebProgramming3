import './App.css';
import { createTheme, ThemeProvider } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './store/store';
import { router } from './router/Router';
import { RouterProvider } from 'react-router-dom';

function App() {

  const theme = createTheme();

  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
     </ThemeProvider>
    </Provider>
  );
}

export default App;
