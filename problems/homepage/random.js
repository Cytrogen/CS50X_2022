// In random.html
// There are four id-s: digimon's icon, digimon's name, digimon's description, and the displaying text in button
// In default, the digimon will be DigiEgg, and the button will display "Touch the DigiEgg!"
// After clicking the button, the digimon will evolve to random digimon, and the button will change to "Evolve!"
// After reaching the Ultimate stage, the button will change to "Get another DigiEgg?"

var digiStage = 0;
var digiIndex = Math.floor(Math.random() * 3) + 1;;

// a is 1
// b is 2
// ...
// The 1st digit -> stage
// The 2nd digit -> index
const digiNames = {
    "aa": "Botamon",
    "ba": "Koromon",
    "ca": "Agumon",
    "da": "Greymon",
    "ea": "Metal Greymon",
    "fa": "War Greymon",

    "ab": "Punimon",
    "bb": "Tunomon",
    "cb": "Gabumon",
    "db": "Garurumon",
    "eb": "Were Garurumon",
    "fb": "Metal Garurumon",

    "ac": "Nyokimon",
    "bc": "Pyocomon",
    "cc": "Piyomon",
    "dc": "Birdramon",
    "ec": "Garudamon",

    "ad": "Bubbmon",
    "bd": "Mochimon",
    "cd": "Tentomon",
    "dd": "Kabuterimon",
    "ed": "Atlur Kabuterimon (Red)",

    "ae": "Yuramon",
    "be": "Tanemon",
    "ce": "Palmon",
    "de": "Togemon",
    "ee": "Lilimon",

    "af": "Pitchmon",
    "bf": "Pukamon",
    "cf": "Gomamon",
    "df": "Ikkakumon",
    "ef": "Zudomon",

    "ag": "Poyomon",
    "bg": "Tokomon",
    "cg": "Patamon",
    "dg": "Angemon",
    "eg": "Holy Angemon",

    "ah": "Yukimi Botamon",
    "bh": "Nyaromon",
    "ch": "Plotmon",
    "dh": "Tailmon",
    "eh": "Angewomon",
};

const digiDesc = {
    // Agumon
    "aa": "A Digital Monster that was born just recently. On the surface of its slime-shaped body, it has grown thick, black fuzz.",
    "ba": "A tiny Digimon that shed the fuzz covering its surface, and whose body grew even bigger. Although it has become able to move around more actively, it is still unable to battle.",
    "ca": "A Reptile Digimon with an appearance resembling a small dinosaur, it has grown and become able to walk on two legs. Its strength is weak as it is still in the process of growing, but it has a fearless and rather ferocious personality.",
    "da": "A Dinosaur Digimon whose cranial skin has hardened so that it is covered in a rhinoceros beetle-like shell. It is an extremely aggressive Digimon, with a body like a lethal weapon covered in sharp claws and gigantic horns.",
    "ea": "A Cyborg Digimon which has mechanized more than half of its body. Metal Greymon's offensive power is said to equal that of a single nuclear warhead, and if the likes of a low-level Digimon suffered that blow, it would be annihilated without leaving a trace.",
    "fa": 'The strongest dragon warrior whose body is clad in armor of the super-metal "Chrome Digizoid", it is the ultimate form of Greymon-species Digimon.',
    // Gabumon
    "ab": "A new kind of newborn Digimon. Its gelatinous red body is squishy, and there are three feeler-like things growing on its head. It is unable to battle, but it can produce resilient, acidic bubbles to intimidate its opponents.",
    "bb": "A tiny Digimon that hardened one of the feelers on its head as Punimon. From Punimon, it has accomplished a more animal-like evolution, and is covered in tufty body hair.",
    "cb": "Although it is covered by a fur pelt, it is clearly a Reptile Digimon. Due to its extremely timid and shy personality, it always gathers up the data which Garurumon leaves behind, and shapes it into a fur pelt to wear.",
    "db": 'Covered in blue, white, and silver-colored fur, it is a Beast Digimon with an appearance resembling a wolf. That fur is as hard as "Mithril", which is said to be a legendary rare metal.',
    "eb": "A Beast Man Digimon that evolved from Garurumon and gained the ability to walk on two legs. Its speed dropped as a result of turning bipedal, but it became a Commando Type Digimon with stronger offensive and defensive power, as well as developed a tactical nature.",
    "fb": "The final form of Garurumon, powered up by metallizing almost its entire body. Not only has it retained its natural keenness when it underwent metallization, but it can also pulverize the opponent with the countless weapons concealed throughout its body.",
    // Piyomon
    "ac": "A Seed Digimon whose body surface is covered in transparent tissue. Its real body can be confirmed to be within the transparent skin, and seems to be a variant of Botamon.",
    "bc": "A Bulb-type Lesser Digimon with a large flower blooming from its head. It is able to move by skillfully operating its root-like tentacles, and with its lightness, it can rise into the air, but only to a small height.",
    "cc": "A Chick Digimon whose wings have developed to become like arms. It is able to dexterously operate its wings and use them to grip objects, but for that reason, it is poor at flying in the air.",
    "dc": "A Giant Bird Digimon which has an appearance shrouded in blazing flames. It flaps its gigantic wings, and flies about the sky.",
    "ec": "A Bird Man Digimon that has gigantic talons and wings that let it dance freely through the sky. Garudamon honors justice and order, and is a guardian deity of the land and wind that loves nature.",
    // Tentomon
    "ad": "Although it looks like it is just pale green bubbles at first glance, it is a Bubble Digimon that can move freely and express a plethora of facial expressions. Because its surface has not hardened yet, its defensive power is nonexistent and it is equally unsuited for combat.",
    "bd": 'Possessing elastic skin, it is a soft-bodied Digimon that uses the protuberances on the underside of its body to toddle about. It came to be called "Mochimon" from inflating its body when it gets worked up, causing it to look like mochi.',
    "cd": "The original type of Insect Digimon who, although it has a hard shell, still has low aggression. It has one hard claw on each of its fore-legs, and four on each of its middle- and hind-legs, and in particular, the middle-legs are able to skillfully grasp objects just like a human hand.",
    "dd": "A fairly unique Insect Digimon, even among newly discovered Digimon. The details of how it evolved into an insect Type are unclear, but it has both ant-like power and the flawless defensive ability possessed by a beetle.",
    "ed": "An evolution of Kabuterimon that was discovered within the tropical region of the Net Area. It is almost 1.5 times Kabuterimon's size, and is quite large among Insect Digimon.",
    // Palmon
    "ae": "A Seed Digimon whose whole body is covered in a substance with the appearance of long, soft hair. When it hatches from its Digitama, it seeks an environment suitable for its growth, and drifts lightly through the air, like a dandelion seed.",
    "be": "A Bulb Digimon which has something that looks like a plant sprout burgeoning from its head. It is a Yuramon that wandered in search of an optimal environment, then settled to the ground and evolved.",
    "ce": "A Plant Digimon with a tropical flower blooming on its head. Although it evolved like a reptile from Tanemon, it is an unusual Type which is classified as a Plant based on its outward appearances and special qualities.",
    "de": "A Plant Digimon which has the appearance of a gigantic cactus. It can store nutrient data within its body, and can even survive for a long time in the empty desert areas.",
    "ee": "A Fairy Digimon born from beautifully blooming flower petals. Although it looks like it has an appearance like a human child, it is a Perfect Digimon hiding unfathomable power within.",
    // Gomamon
    "af": 'A microbe-like Digimon which was discovered in the "Net Ocean", which had long been studied as the birthplace of life within the Digital World, it has the smallest size among the many Digimon.',
    "bf": "Although it has an appearance which is thought to be the infancy of an aquatic dinosaur, it is a funny Digimon with movements as clever as the seahorse. However, the friendly personality it had as Pitchmon has totally vanished, and it quickly flees if others approach.",
    "cf": "A Marine Animal Digimon that became able to move on land, and is covered in temperature-maintaining fur. The short, white fur that covers its body gets longer as it grows, and furthermore, it's said that it turns brown when it grows up.",
    "df": 'A marine animal Digimon that was discovered in the computer of an Arctic exploration base. Its sharp horn is made of "Mithril", one of the rare metals, and the skin under its fur is just as hard.',
    "ef": "Ikkakumon evolved further, and as a Power Digimon it became able to walk on two legs. It further guards its well-tempered muscles with protectors, which it made from the pelt and shell that it stole from its opponents.",
    // Patamon
    "ag": 'With a translucent body, it is a Digimon Baby that drifts through the "Net Ocean" like a jellyfish. In order to defend itself from intruders it spews potently acidic bubbles out of its mouth.',
    "bg": "A tiny Digimon with limb-like protrusions growing beneath its body (head?). Baby Digimon that have grown limbs are extremely rare, and their appearance is enormously cute.",
    "cg": "A Mammal Digimon characterized by its large ears. It is able to fly through the air by using them as large wings, but because it only goes at a speed of 1 km/h, it is said that it is definitely faster walking.",
    "dg": "An Angel Digimon with six shining wings, whose body is clad in cloth so pure white as to be divine. When confronting evil it does not stop attacking, with extreme composure, until the opponent is completely annihilated.",
    "eg": "An Archangel Digimon with eight shining, silver wings. Holy Angemon's mission in the Digital World is to act as a law enforcement officer, and it has the duty of supervising and surveying the masses of Angel Digimon.",
    // Tailmon
    "ah": 'A Baby Digimon whose whole body is covered in fluffy, white hair. It is considered a species of Botamon, and was named "Yukimi Botamon" after its white body, but the details are not clearly known.',
    "bh": 'A tiny Digimon which has cat-like characteristics. It is always capricious, and that behavior seems to have been attached to Nyaromon as a result of its being like a "cat".',
    "ch": "A Holy-species Digimon child characterized by its lop ears. Because it is still very young, it is unable to manifest its holy powers, and isn't even aware of its own mission.",
    "dh": "It has a very healthy curiosity, so it loves pranks. Although its body is small, it is a precious Holy-species Digimon, and its appearance does not match the true strength it possesses. ",
    "eh": "An Archangel Digimon with the appearance of a beautiful woman. Although it was previously classified as an Angel-type, it was confirmed as an Archangel-type because of the greatness of its abilities."
}

// function button_change() {
//     document.getElementById('random_button').innerHTML = "Evolve!";
// }

// function description_change() {
//     document.getElementById('random_description').innerHTML = "On the surface of its slime-shaped body, it has grown thick, black fuzz.";
//     button_change();
// }

// function name_change() {
//     var n = "n" + digiStage + "_" + digiIndex;
//     document.getElementById('random_name').innerHTML = digiNames.n;
//     description_change();
// }

function reset_everything() {
    digiStage = 0;
    source = "image/randoms/360px-Digitama.jpg";
    document.getElementById('random_icon').src=source;
    document.getElementById('random_name').innerHTML = 'DigiEgg';
    document.getElementById('random_description').innerHTML = "Or Digitama. They're eggs from which Digimons are born, also the end of all Digimons.";
}

function icon_change() {
    digiStage += 1;
    // Change the image source
    var source = "image/randoms/" + digiStage + "/" + digiIndex + ".jpg";
    document.getElementById('random_icon').src=source;

    // Change the name
    // Convert number to letter
    var numberA = String.fromCharCode(96 + digiStage);
    var numberB = String.fromCharCode(96 + digiIndex);
    var n = numberA + numberB;
    document.getElementById('random_name').innerHTML = digiNames[n];

    // Change the description
    document.getElementById('random_description').innerHTML = digiDesc[n];

    // Change the button
    // When the digiIndex is 1 and 2
    if (digiIndex <= 2) {
        if (digiStage == 6) {
            document.getElementById('random_button').innerHTML = "Hatch another DigiEgg?";
        } else if (digiStage >= 7) {
            reset_everything();
            document.getElementById('random_button').innerHTML = "Touch the DigiEgg!";
            digiIndex = Math.floor(Math.random() * 8) + 1;
        } else {
            document.getElementById('random_button').innerHTML = "Evolve!";
        }
    } else {
        if (digiStage == 5) {
            document.getElementById('random_button').innerHTML = "Hatch another DigiEgg?";
        } else if (digiStage >= 6) {
            reset_everything();
            digiIndex = Math.floor(Math.random() * 8) + 1;
            document.getElementById('random_button').innerHTML = "Touch the DigiEgg!";
        } else {
            document.getElementById('random_button').innerHTML = "Evolve!";
        }
    }
}