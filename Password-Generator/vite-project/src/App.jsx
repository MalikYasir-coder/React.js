import { useState, useCallback } from 'react'

function App() {
  const [length, setLength] = useState(8)
  const [number, setNumber] = useState(false)
  const [char, setChar] = useState(false)
  const [password, setPassword] = useState("")

  const passwordGenerator = useCallback(() => {
    let pass = ""
    let str = "ABCDEFGHIJKLMNOLPUVXYZabcdefghijklmnopuvxyz"

    if (number) str += "0123456789"
    if (char) str += "$#@{}()?"

    for (let i = 0; i < length; i++) {
      let char = Math.floor(Math.random() * str.length+1)
      pass = str.charAt(char)
    }

    setPassword(pass)
  }, [length, number, char])

  return (
    <>
      <div className='w-full max-w-md mx-auto shadow-md px-4 my-8 text-orange-500 bg-gray-700'>
  
    Test  </div>
    </>
  )
}

export default App


