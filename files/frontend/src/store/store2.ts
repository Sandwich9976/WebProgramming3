//лекция 14.1
import { configureStore } from '@reduxjs/toolkit'
import authReducer from "./authSlice"
import { authApi } from './authApi'
import { reviewApi } from './reviewApi'

export const store2 = configureStore({
    reducer: {
        auth: authReducer,
        [authApi.reducerPath]: authApi.reducer,
        [reviewApi.reducerPath]: reviewApi.reducer
    }, 
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat([authApi.middleware, reviewApi.middleware]),
})



export type RootState = ReturnType<typeof store2.getState>
//Функция, с помощью которой отправляем данные из наших компонентов
export type AppDispatch = typeof store2.dispatch
