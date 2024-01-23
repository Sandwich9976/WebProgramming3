import { configureStore } from '@reduxjs/toolkit'
import counterReducer from "./counterSlice"
import { authApi } from './authApi'

export const store = configureStore({
    //Специальная функция, которая изменяет состояние приложения
    reducer: {
        counter: counterReducer,
        [authApi.reducerPath]: authApi.reducer
    }, 
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(authApi.middleware),
})



export type RootState = ReturnType<typeof store.getState>
//Функция, с помощью которой отправляем данные из наших компонентов
export type AppDispatch = typeof store.dispatch
