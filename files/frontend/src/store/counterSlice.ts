import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'

interface CounterState {
  value: number
}
//Задаём начальные значения. При этом в этой функции могут быть указаны только тое значения, которые указаны в одноимённой функции интерфейса
const initialState:CounterState = { value: 0 }

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  //Reducers изменяют наше состояние
  reducers: {
    increment(state) {
      state.value++
    },
    decrement(state) {
      state.value--
    },
    incrementByAmount(state, action: PayloadAction<number>) {
      state.value += action.payload
    },
  },
})

export const { increment, decrement, incrementByAmount } = counterSlice.actions
export default counterSlice.reducer