async function getAPI(city){
    const API_KEY = "87b173240bc0ad3142684a58b4b02d01"
    const API_URL = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`
    const response = await fetch(API_URL);
    const json = await response.json();
    return json;
}

function setImage(weather){
    console.log(weather);
    const image = document.querySelector('.weather-box img');

    const Images = {
        "Clear" : 'images/clear.png',
        'Rain' : 'images/rain.png',
        'Snow' : 'images/snow.png',
        'Clouds' : 'images/cloud.png',
        'Haze' : 'images/mist.png',
    }

    if(Images[weather]){
        image.src = Images[weather];
    }
    else{
       image.src = '' ;
    }
}

function setBackground(temperature) {
    const body = document.body;
    let gradient = '';

    if (temperature <= 0) {
        gradient = 'radial-gradient(circle, #00f, #99f)';
    } else if (temperature > 0 && temperature <= 10) {
        gradient = 'radial-gradient(circle, #99f, #ccf)';
    } else if (temperature > 10 && temperature <= 20) {
        gradient = 'radial-gradient(circle, #ccf, #fff)';
    } else if (temperature > 20 && temperature <= 30) {
        gradient = 'radial-gradient(circle, #fff, #fc9)';
    } else {
        gradient = 'radial-gradient(circle, #fc9, #f00)';
    }

    body.style.background = gradient;
}

const container = document.querySelector('.container');
const search = document.querySelector('.search-box button');
const weatherBox = document.querySelector('.weather-box');
const weatherDetails = document.querySelector('.weather-details');
const error404 = document.querySelector('.not-found');

search.addEventListener('click', async (e) => {
    const city = document.querySelector('.search-box input').value;

    if (!city) {
        console.log('도시를 입력해주세요.');
        return;
    }
    const json = await getAPI(city);

    if (json.cod === '404') {
        container.style.height = '400px';
        weatherBox.style.display = 'none';
        weatherDetails.style.display = 'none';
        error404.style.display = 'block';
        error404.classList.add('fadeIn');
        return;
    }

    error404.style.display = 'none';
    error404.classList.remove('fadein');
    
    const temperature = document.querySelector('.weather-box .temperature');
    const description = document.querySelector('.weather-box .description');
    const humidity = document.querySelector('.weather-details .humidity span');
    const wind = document.querySelector('.weather-details .wind span');
    
    setImage(json.weather[0].main);
    temperature.innerHTML = `${parseInt(json.main.temp)}<span>°C</span>`;
    description.innerHTML = `${json.weather[0].description}`;
    humidity.innerHTML = `${json.main.humidity}%`;
    wind.innerHTML = `${parseInt(json.wind.speed)}Km/h`;

    setBackground(parseInt(json.main.temp));

    weatherBox.style.display = '';
    weatherDetails.style.display = '';
    weatherBox.classList.add('fadeIn');
    weatherDetails.classList.add('fadeIn');
    container.style.height = '590px';
});
