import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import Chart from 'chart.js/auto';
import axios from 'axios';

// Chart.js의 구성 요소를 명시적으로 등록
Chart.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

// 날짜 형식을 변경하는 함수
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${month}:${day} ${hours}:${minutes}`;
}

const PlantEnvironmentChart = () => {
    const [environmentData, setEnvironmentData] = useState(null);

    useEffect(() => {
        // 환경 데이터 가져오기
        axios
            .get('http://localhost:8000/api/plant/get-env')
            .then((response) => {
                // 최근 30개 데이터만 가져오기
                const recentData = response.data.slice(-30);
                // 날짜 데이터 변환 및 추출
                const labels = recentData.map((item) => formatDate(item.date));
                // 온도 데이터 추출
                const temperatureData = recentData.map(
                    (item) => item.temperature
                );
                // 습도 데이터 추출
                const humidityData = recentData.map((item) => item.humidity);
                // 조명 데이터 추출
                const illuminationData = recentData.map(
                    (item) => item.illumination
                );

                // 차트 데이터 설정
                setEnvironmentData({
                    labels: labels,
                    datasets: [
                        {
                            label: 'Temperature',
                            data: temperatureData,
                            borderColor: 'red',
                            borderWidth: 1,
                        },
                        {
                            label: 'Humidity',
                            data: humidityData,
                            borderColor: 'blue',
                            borderWidth: 1,
                        },
                        {
                            label: 'Illumination',
                            data: illuminationData,
                            borderColor: 'green',
                            borderWidth: 1,
                        },
                    ],
                });
            })
            .catch((error) => {
                console.error('Error fetching environment data:', error);
            });
    }, []);

    return (
        <div>
            <h2 className="text-xl font-semibold mb-4">
                식물 환경 정보 그래프
            </h2>
            <hr />
            {environmentData && <Line data={environmentData} />}
        </div>
    );
};

export default PlantEnvironmentChart;
