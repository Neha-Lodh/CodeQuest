const hero = document.querySelector(".hero");

function enterWorld(id, event){

    event.preventDefault();

    let world =
        document.getElementById("world"+id);

    let rect =
        world.getBoundingClientRect();

    hero.style.transition = "all 1.2s ease";

    hero.style.left = rect.left + 70 + "px";

    hero.style.top = rect.top + 40 + "px";

    playWalk();

    setTimeout(()=>{

        window.location =
        "/world/"+id;

    },1300);

}