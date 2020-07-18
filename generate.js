var foods = [
  "alfalfa",
  "shawarma",
  "gin",
  "rum",
  "tea",
  "tomago",
  "beetroot",
  "tunip",
  "cardamom",
  "fried",
  "boiled",
  "baked",
  "steamed",
  "broiled",
  "sake",
  "tequila",
  "blueberry",
  "biryani",
  "clover",
  "apricot",
  "pea",
  "bean",
  "lentil",
  "lupin",
  "mesquite",
  "carob",
  "soybean",
  "peanut",
  "tamarind",
  "acorn",
  "almond",
  "beech",
  "candlenut",
  "cashew",
  "chestnut",
  "hazelnut",
  "pecan",
  "macadamia",
  "pistachio",
  "walnut",
  "asparagus",
  "apple",
  "avacado",
  "squash",
  "arugala",
  "artichoke",
  "applesauce",
  "noodle",
  "cantelope",
  "tuna",
  "juice",
  "sushi",
  "bruscetta",
  "bacon",
  "bagel",
  "bbq",
  "bison",
  "barley",
  "beer",
  "bisque",
  "bluefish",
  "bread",
  "broccoli",
  "buritto",
  "babaganoosh",
  "cabbage",
  "cake",
  "carrots",
  "celery",
  "cheese",
  "chicken",
  "catfish",
  "chips",
  "chocolate",
  "chowder",
  "clam",
  "coffee",
  "cookie",
  "corn",
  "cupcake",
  "crab",
  "curry",
  "cereal",
  "chimichanga",
  "date",
  "dip",
  "duck",
  "dumpling",
  "donut",
  "egg",
  "enchilada",
  "eggroll",
  "muffin",
  "edamame",
  "eel",
  "fajita",
  "falafel",
  "fish",
  "fondu",
  "toast",
  "garlic",
  "ginger",
  "gnocchi",
  "goose",
  "granola",
  "grape",
  "guacamole",
  "gumbo",
  "grits",
  "cracker",
  "ham",
  "halibut",
  "hamburger",
  "cheeseburger",
  "honey",
  "sugar",
  "roll",
  "hummus",
  "ice",
  "cream",
  "stew",
  "jambalaya",
  "jelly",
  "jam",
  "jerky",
  "jalapeño",
  "kale",
  "ketchup",
  "kiwi",
  "kingfish",
  "lobster",
  "lamb",
  "linguine",
  "lasagna",
  "meatball",
  "moose",
  "milk",
  "milkshake",
  "ostrich",
  "pizza",
  "pepperoni",
  "pancakes",
  "quesadilla",
  "quiche",
  "reuben",
  "spinach",
  "spaghetti",
  "venison",
  "waffle",
  "wine",
  "yogurt",
  "ziti",
  "zucchini",
  "water",
  "vodka",
  "cocktail",
  "rhubarb",
  "martini",
  "watermelon",
  "melon",
  "strawberry",
  "raspberry",
  "banana",
  "cherry",
  "lemon",
  "plum",
  "pumpkin",
  "potato",
  "eggplant",
  "onion",
  "mushroom",
  "sausage",
  "steak",
  "porridge",
  "rice",
  "seafood",
  "cod",
  "herring",
  "salmon",
  "maize",
  "wheat",
  "flour",
  "musturd",
  "crisp",
  "syrup",
  "candy",
  "dessert",
  "kebab",
  "kombucha",
  "pie",
  "salad",
  "letuce",
  "sandwich",
  "sauce",
  "soy",
  "snack",
  "raisin",
  "soup",
  "cider",
  "soda",
  "pop",
  "alcohol",
  "lemonade",
  "marshmallow",
];

var button = [
  "Generate",
  "Generate Recipe",
  "Generate Password",
  "Generate Recipe Password",
  "Generate Random Password",
  "Generate Random Recipe",
  "Another!",
  "Not your cup of tea?",
  "Still hungry?",
];

var placeholders = ["correct-horse-battery-staple", "water-rhubarb-martini"];

function starter() {
  document.getElementById("pass").innerHTML =
    placeholders[Math.floor(Math.random() * placeholders.length)];
}

function pass(btn) {
  var slider = 4;
  var slider = document.getElementById("myRange");
  var randFoods = [];
  var generated = "";

  for (var i = 0; i < slider.value; i++) {
    randFoods.push(foods[Math.floor(Math.random() * foods.length)]);
    randFoods.push("-");
  }

  for (var i = 0; i < slider.value * 2 - 1; i++) {
    generated += randFoods[i];
  }

  document.getElementById("pass").innerHTML = generated;

  if (btn) {
    document.getElementById("gen").innerHTML =
      button[Math.floor(Math.random() * button.length)];
  }
}

function menu() {
  var menu = document.getElementById("menu");
  if (menu.style.display === "block") {
    menu.style.display = "none";
  } else {
    menu.style.display = "block";
  }
}

var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value; // Display the default slider value

function slide() {
  range_weight_disp.value = myRange.value;
  pass();
}
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
  output.innerHTML = this.value;
  pass(false);
};
