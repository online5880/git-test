// app.js
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const explodeBtn = document.getElementById('explodeBtn');

const randomImageUrl = 'https://media1.giphy.com/media/gEKz4VLX7fQlsl8SFE/giphy.webp?cid=790b7611bm66rxquxqlwyr16wl2yvrg002kgds7lemstqep6&ep=v1_gifs_search&rid=giphy.webp&ct=g';

let image = new Image();
image.src = randomImageUrl;
image.onload = () => {
    ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
};

const { Engine, Render, World, Bodies, Body, Events } = Matter;

const engine = Engine.create();
const world = engine.world;

const render = Render.create({
    canvas: canvas,
    engine: engine,
    options: {
        width: 800,
        height: 600,
        wireframes: false,
        background: 'transparent'
    }
});

Render.run(render);
Engine.run(engine);

explodeBtn.addEventListener('click', () => {
    explodeImage();
});

function explodeImage() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let parts = [];
    const partWidth = canvas.width / 10;
    const partHeight = canvas.height / 10;

    for (let y = 0; y < 10; y++) {
        for (let x = 0; x < 10; x++) {
            const imageData = ctx.getImageData(x * partWidth, y * partHeight, partWidth, partHeight);
            const texture = new Image();
            texture.src = randomImageUrl;
            texture.onload = () => {
                const part = Bodies.rectangle(x * partWidth + partWidth / 2, y * partHeight + partHeight / 2, partWidth, partHeight, {
                    render: {
                        sprite: {
                            texture: texture.src,
                            xScale: 0.1,
                            yScale: 0.1
                        }
                    }
                });
                parts.push(part);
                World.add(world, part);
            };
        }
    }

    Events.on(engine, 'afterUpdate', () => {
        if (parts.length > 0) {
            parts.forEach(part => {
                Body.applyForce(part, { x: part.position.x, y: part.position.y }, { x: (Math.random() - 0.5) * 0.05, y: (Math.random() - 0.5) * 0.05 });
            });
            parts = [];
        }
    });
}
