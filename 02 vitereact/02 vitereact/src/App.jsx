import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { use } from 'react'

function App() {
  let [counter,setCounter] = useState(15)
  // const [count, setCount] = useState(0)
  // let counter =15
  const addvalue  = () => {
    console.log("value added", Math.random())
    setCounter(counter = counter+1)
  }
  const removevalue = () =>{
    setCounter(counter = counter-1)
  }

  return (
    <>
      <h1>Vite + React</h1>
      <h2>Counter Value:{counter} </h2>
      <button
      onClick={addvalue}>Add Value</button>
      <br/>
      <button
      onClick={removevalue}>Remove Value</button>
    </>
  )
}

export default App
