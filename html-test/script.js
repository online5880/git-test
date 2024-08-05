const calculator = {
    displayValue: '0',
    firstOperand: null,
    waitingForSecondOperand: false,
    operator: null,
};

function inputDigit(digit) {
    const { displayValue, waitingForSecondOperand } = calculator;

    if (waitingForSecondOperand === true) {
        calculator.displayValue = digit;
        calculator.waitingForSecondOperand = false;
    } else {
        calculator.displayValue = displayValue === '0' ? digit : displayValue + digit;
    }
}

function inputDecimal(dot) {
    if (calculator.waitingForSecondOperand === true) return;

    if (!calculator.displayValue.includes(dot)) {
        calculator.displayValue += dot;
    }
}

function handleOperator(nextOperator) {
    const { firstOperand, displayValue, operator } = calculator;
    const inputValue = parseFloat(displayValue);

    if (operator && calculator.waitingForSecondOperand) {
        calculator.operator = nextOperator;
        return;
    }

    if (firstOperand == null && !isNaN(inputValue)) {
        calculator.firstOperand = inputValue;
    } else if (operator) {
        const result = performCalculation[operator](firstOperand, inputValue);

        calculator.displayValue = String(result);
        calculator.firstOperand = result;
    }

    calculator.waitingForSecondOperand = true;
    calculator.operator = nextOperator;
}

const performCalculation = {
    '/': (firstOperand, secondOperand) => firstOperand / secondOperand,
    '*': (firstOperand, secondOperand) => firstOperand * secondOperand,
    '+': (firstOperand, secondOperand) => firstOperand + secondOperand,
    '-': (firstOperand, secondOperand) => firstOperand - secondOperand,
    '=': (firstOperand, secondOperand) => secondOperand
};

function resetCalculator() {
    calculator.displayValue = '0';
    calculator.firstOperand = null;
    calculator.waitingForSecondOperand = false;
    calculator.operator = null;
}

function updateDisplay() {
    const display = document.querySelector('.calculator-screen');
    display.value = calculator.displayValue;
}

function explodeCalculator() {
    const calculatorElement = document.querySelector('.calculator');
    const fragments = [];
    const fragmentSize = 40;
    const rows = Math.ceil(calculatorElement.clientHeight / fragmentSize);
    const cols = Math.ceil(calculatorElement.clientWidth / fragmentSize);

    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const fragment = document.createElement('div');
            fragment.classList.add('fragment');
            fragment.style.width = `${fragmentSize}px`;
            fragment.style.height = `${fragmentSize}px`;
            fragment.style.top = `${y * fragmentSize}px`;
            fragment.style.left = `${x * fragmentSize}px`;
            document.getElementById('calculator-container').appendChild(fragment);
            fragments.push(fragment);
        }
    }

    const { Engine, Render, Runner, Bodies, Composite } = Matter;

    const engine = Engine.create();
    const render = Render.create({
        element: document.getElementById('calculator-container'),
        engine: engine,
        options: {
            width: calculatorElement.clientWidth,
            height: calculatorElement.clientHeight,
            wireframes: false,
            background: 'transparent'
        }
    });

    const ground = Bodies.rectangle(calculatorElement.clientWidth / 2, calculatorElement.clientHeight + 10, calculatorElement.clientWidth, 10, { isStatic: true });
    const walls = [
        Bodies.rectangle(-10, calculatorElement.clientHeight / 2, 10, calculatorElement.clientHeight, { isStatic: true }),
        Bodies.rectangle(calculatorElement.clientWidth + 10, calculatorElement.clientHeight / 2, 10, calculatorElement.clientHeight, { isStatic: true }),
        Bodies.rectangle(calculatorElement.clientWidth / 2, -10, calculatorElement.clientWidth, 10, { isStatic: true })
    ];

    Composite.add(engine.world, [ground, ...walls]);

    fragments.forEach(fragment => {
        const body = Bodies.rectangle(
            fragment.offsetLeft + fragmentSize / 2,
            fragment.offsetTop + fragmentSize / 2,
            fragmentSize,
            fragmentSize
        );
        fragment.style.position = 'absolute';
        Composite.add(engine.world, body);
        Matter.Events.on(engine, 'afterUpdate', () => {
            fragment.style.left = `${body.position.x - fragmentSize / 2}px`;
            fragment.style.top = `${body.position.y - fragmentSize / 2}px`;
            fragment.style.transform = `rotate(${body.angle}rad)`;
        });
    });

    Render.run(render);
    const runner = Runner.create();
    Runner.run(runner, engine);
}

updateDisplay();

const keys = document.querySelector('.calculator-keys');
keys.addEventListener('click', (event) => {
    const { target } = event;
    if (!target.matches('button')) {
        return;
    }

    if (target.classList.contains('operator')) {
        handleOperator(target.value);
        updateDisplay();
        return;
    }

    if (target.classList.contains('decimal')) {
        inputDecimal(target.value);
        updateDisplay();
        return;
    }

    if (target.classList.contains('all-clear')) {
        resetCalculator();
        updateDisplay();
        return;
    }

    if (target.classList.contains('equal-sign')) {
        handleOperator(target.value);
        updateDisplay();
        explodeCalculator(); // 물리적 폭발 효과 트리거
        return;
    }

    inputDigit(target.value);
    updateDisplay();
});
