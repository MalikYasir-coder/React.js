function customRender(reactElement, container){
    const domElement = document.createElement(reactElement.type)   
    domElement.innerHTML = reactElement.children
    for (const props in reactElement.props) {
      domElement.setAttribute(prop,reactElement.props[prop])
        
    }
    // domElement.setAttribute('href',reactElement.props.href)


    container.appendChild(domElement)

}


 const reactElement = {
    type :'a',
    props:{
        href:'https://google.com'
    },
    children:'click me to visit google'
 }
 
 
 
 const container = document.querySelector("#root")
 customRender(reactElement,container);