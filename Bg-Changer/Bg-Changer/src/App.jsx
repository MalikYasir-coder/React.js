import { useState } from "react";

function App(){
   const [color,setColor] = useState("olive")

   return (
  <div 
    style={{ 
      backgroundColor: color, 
      width: '100vw', 
      height: '100vh', 
      transition: '0.2s' 
    }}
  >
    <div className="fixed flex flex-wrap justify-center bottom-12 inset-x-0 px-2">
    <div className="flex flex-wrap justify content gap-3 shadow-lg bg-white px-2 py-3 rounded-3xl" >
     <button
      onClick={() => setColor("red")}
      className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"red"}}>Red</button>
        <button
         onClick={() => setColor("green")}
         className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"green"}}>Green</button>
        <button
         onClick={() => setColor("blue")}
         className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"blue"}}>Blue</button>
        <button
         onClick={() => setColor("yellow")}
         className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"yellow"}}>Yellow</button>
        <button
         onClick={() => setColor("grey")}
         className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"grey"}}>Grey</button>
        <button 
         onClick={() => setColor("black")}
         className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"black"}}>Black</button>
        <button 
         onClick={() => setColor("grey")}
        className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"grey"}}>Grey</button>
        <button 
         onClick={() => setColor("grey")}
        className="outline-none px-4 rounded full text-white  shadow-lg"
     style={{backgroundColor:"grey"}}>Grey</button>

      </div>
      </div>
    {/* Content goes here */}
  </div>
);
}

export default App

