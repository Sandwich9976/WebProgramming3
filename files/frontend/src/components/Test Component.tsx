import {Box, Button} from "@mui/material"
import { useDispatch, useSelector } from "react-redux"
import { RootState } from "../store/store"
import { decrement, increment } from "../store/counterSlice"

export const TestComponent = ()=>{
    const value = useSelector((state: RootState)=>state.counter.value)

    const dispatch = useDispatch()

    return <>
    <Box>{value}</Box>
    <Button variant={"outlined"} onClick={()=>{dispatch(increment())}}>Increase!</Button>
    <Button variant={"outlined"} onClick={()=>{dispatch(decrement())}}>Decrease!</Button>
    <Button variant={"contained"}>Le simple buttone</Button></>
}
