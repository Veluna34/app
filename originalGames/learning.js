const canvas = document.getElementById('canvas1');
const ctx = canvas.getContext('2d');
const canvasWidth=canvas.width=600;
const canvasHeight=canvas.height=600;

const playerImage=new Image();
playerImage.src='../images/shadow_dog.png';
const spriteWidth=575;
const spriteHeight=523;
let framex=0;
let framey=0;
let gameFrame=0;
const staggerFrames=6;


function animate(){
    ctx.clearRect(0,0,canvasWidth, canvasHeight);
    //ctx.fillRect(x,50,100, 100);
    ctx.drawImage(playerImage, framex * spriteWidth, framey * spriteHeight, spriteWidth, spriteHeight, 0, 0, spriteWidth, spriteHeight);
    requestAnimationFrame(animate);
    if(gameFrame % staggerFrames == 0){
        if (framex<6) framex++;
        else framex=0;
    }

    gameFrame++
    
}
animate();

