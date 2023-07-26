// const ingredientsBtn = document.querySelector("#ingredients-btn")
// ingredientsBtn.addEventListener("click", function (e) {
//   e.preventDefault()
//   console.log("button click");
//   const ingredient = document.querySelector("#ingredient")
//   const ingredientVal = ingredient.value
//   const ingredientIndex = parseInt(ingredientVal) + 1
//   console.log(ingredientIndex);
//   const ingredientText = ingredient.children[ingredientIndex].textContent
//   const ingredientId = ingredient.children[ingredientIndex].getAttribute("ingredientId")
//   console.log(ingredientId);

//   const quantity = document.querySelector("#quantity").value
//   const unit = document.querySelector("#unit").value

//   unitObj = {
//     "1": "cup",
//     "2": "ml",
//     "3": "g",
//   }
//   unitName = unitObj[unit]

//   const ingredientsList = document.querySelector("#ingredientsList")

//   const ul = document.createElement("ul")
//   const li = document.createElement("li")
//   li.textContent = `${ingredientText}  - ${quantity} ${unitName}`

//   var ingredientObj = {
//     id: ingredientId,
//     quantity: quantity,
//   }
//   var ingredients = []


//   // const input = document.createElement("input")
//   // input.setAttribute("name", "test")
//   // input.setAttribute("value", `${ingredientVal}, ${quantity}`)

//   // input.textContent = `${ingredientText} - ${quantity} - ${unit}`
//   // li.appendChild(input)
//   ul.appendChild(li)
//   ingredientsList.appendChild(ul)
// })

