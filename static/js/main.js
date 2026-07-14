// =============================
// Success Popup
// =============================

function showSuccess(message){

    const popup=document.createElement("div");

    popup.className="popup success-popup";

    popup.innerHTML=`
        <h2>🎉 Challenge Completed!</h2>
        <p>${message}</p>
    `;

    document.body.appendChild(popup);

    setTimeout(()=>{

        popup.classList.add("show");

    },100);

    setTimeout(()=>{

        popup.classList.remove("show");

        setTimeout(()=>{
            popup.remove();
        },500);

    },2500);

}

// =============================
// XP Popup
// =============================

function showXP(xp){

    const xpBox=document.createElement("div");

    xpBox.className="xp-popup";

    xpBox.innerHTML=`⭐ +${xp} XP`;

    document.body.appendChild(xpBox);

    setTimeout(()=>{

        xpBox.classList.add("show");

    },100);

    setTimeout(()=>{

        xpBox.remove();

    },2500);

}

// =============================
// Level Up
// =============================

function levelUp(level){

    const box=document.createElement("div");

    box.className="level-popup";

    box.innerHTML=`
    <h1>🏆 LEVEL UP!</h1>

    <h2>Level ${level}</h2>
    `;

    document.body.appendChild(box);

    setTimeout(()=>{

        box.classList.add("show");

    },100);

    setTimeout(()=>{

        box.remove();

    },3000);

}

// =============================
// Toast
// =============================

function showToast(message){

    const toast=document.createElement("div");

    toast.className="toast";

    toast.innerHTML=message;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.classList.add("show");

    },100);

    setTimeout(()=>{

        toast.remove();

    },3000);

}
function showCoins(amount){

const box=document.createElement("div");

box.className="coin-popup";

box.innerHTML="🪙 +"+amount+" Coins";

document.body.appendChild(box);

setTimeout(()=>{

box.classList.add("show");

},100);

setTimeout(()=>{

box.remove();

},2500);

}
function unlockAchievement(title){

const box=document.createElement("div");

box.className="achievement";

box.innerHTML=`

🏅 Achievement Unlocked

<h2>${title}</h2>

`;

document.body.appendChild(box);

setTimeout(()=>{

box.classList.add("show");

},100);

setTimeout(()=>{

box.remove();

},3500);

}