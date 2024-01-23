import {createBrowserRouter} from "react-router-dom";
import { Auth } from "../auth/Auth";
import { TestComponent } from "../components/Test Component";
import { Authorized } from "../authorized/Authorized";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <><div>Hello world!</div><h1>Test</h1>
        <TestComponent/></>,
      },
      {
        path: "/auth",
        element: <Auth/>,
      },
      {
        path: "/authorized",
        element: <Authorized/>,
      },
]);
