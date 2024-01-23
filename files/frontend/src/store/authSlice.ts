import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'

enum Roles{
    user="user",
    admin="admin"
}

interface AuthState {
  token: string | null;
  isAuthorized: boolean;
  role: Roles | null
  userId: null | number
}
//Задаём начальные значения. При этом в этой функции могут быть указаны только тое значения, которые указаны в одноимённой функции интерфейса
const initialState:AuthState = { 
    token: null,
    isAuthorized: false,
    role: null,
    userId: null
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  //Reducers изменяют наше состояние
  reducers: {
    setToken:(state, action: PayloadAction<string>) => {
        state.token = action.payload
        state.isAuthorized = true
    },
    invalidateToken:(state) => {
        state.token = null
        state.isAuthorized = false
        state.role = null
    },  
    setRole:(state, action: PayloadAction<string>) => {
        state.token = action.payload
    },
    setUserId:(state, action: PayloadAction<number>) => {
        state.userId = action.payload
    },
  },
})

export const { setToken, invalidateToken, setRole, setUserId } = authSlice.actions
export default authSlice.reducer