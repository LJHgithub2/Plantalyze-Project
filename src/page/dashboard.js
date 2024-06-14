import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import PlantEnvironmentChart from '../components/PlantEnvironmentChart';

const handleControlClick = (type) => {
    var api_path = `http://localhost:9000/${type}`;
    axios
        .get(api_path)
        .then((response) => {
            console.log(`${type} control response:`, response.data);
        })
        .catch((error) => {
            console.error(`${type} control error:`, error);
        });
};

const PlantDashboard = () => {
    const [plantData, setPlantData] = useState(null);

    useEffect(() => {
        axios
            .get('http://localhost:8000/api/plant/latest-plant/')
            .then((response) => {
                setPlantData(response.data);
            })
            .catch((error) => {
                console.error('Error fetching plant data:', error);
            });
    }, []);

    return (
        <div className="flex flex-col items-center p-6 font-sans min-h-screen bg-gray-50">
            {/* 식물 정보 섹션 */}
            <section className="flex flex-col lg:flex-row w-full max-w-4xl mb-8 bg-white p-6 rounded-lg shadow-md">
                <div className="flex-1 mr-6">
                    {plantData && plantData.image ? (
                        <img
                            src={plantData.image}
                            alt="Plant"
                            className="w-full size-96 rounded-lg shadow-md"
                        />
                    ) : (
                        <img
                            src="https://via.placeholder.com/300x200.png?text=Plant+Image"
                            alt="Plant"
                            className="w-full size-96 rounded-lg shadow-md"
                        />
                    )}
                </div>
                <div className="flex-1 flex flex-col mx-4">
                    <h2 className="text-2xl font-bold mb-4 text-center">
                        최근 분석 결과
                    </h2>
                    <div className="pl-9 bg-gray-100 content-center flex-1 flex flex-col">
                        {plantData ? (
                            <>
                                <div className="flex-1 flex py-3">
                                    <div className="flex-3 font-bold content-center">
                                        식물 종류:
                                    </div>
                                    <div className="px-5 flex-1 content-center">
                                        {plantData.plant_type}
                                    </div>
                                </div>
                                <hr></hr>
                                <div className="flex-1 flex">
                                    <div className="flex-3 font-bold content-center">
                                        예측 질병:
                                    </div>
                                    <div className="px-5 flex-1 content-center">
                                        {plantData.predicted_disease}
                                    </div>
                                </div>
                                <hr></hr>
                                <div className="flex-1 flex">
                                    <div className="flex-3 font-bold content-center">
                                        상태 위험도:
                                    </div>
                                    <div className="px-5 flex-1 content-center">
                                        {plantData.risk_level}
                                    </div>
                                </div>
                                <hr></hr>
                                <div className="flex-1 flex">
                                    <div className="flex-3 font-bold content-center">
                                        현재 상태:
                                    </div>
                                    <div className="px-5 flex-1 content-center">
                                        {plantData.current_status}
                                    </div>
                                </div>
                                <hr></hr>
                                <div className="flex-1 flex mb-3">
                                    <div className="flex-3 font-bold content-center">
                                        개선방안:
                                    </div>
                                    <div className="px-5 flex-1 content-center">
                                        {plantData.improvement_plan}
                                    </div>
                                </div>
                            </>
                        ) : (
                            <div>로딩 중...</div>
                        )}
                    </div>
                </div>
            </section>

            {/* 식물 수동 제어 섹션 */}
            <section className="w-full max-w-4xl mb-8">
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-2xl mb-5 font-semibold">
                        식물 수동 제어
                    </h2>
                    <hr />
                    <div className="flex mx-7 mb-5 mt-5 justify-between">
                        <Button
                            variant="contained"
                            color="primary"
                            className="mr-5"
                            onClick={() => handleControlClick('run2')}
                        >
                            펌프 제어
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            className="mr-5"
                            onClick={() => handleControlClick('run3')}
                        >
                            바람 제어
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            className="mr-5"
                            onClick={() => handleControlClick('run1')}
                        >
                            조명 제어
                        </Button>
                    </div>
                </div>
            </section>

            {/* 식물 환경 그래프 섹션 */}
            <section className="w-full max-w-4xl mb-8 bg-white p-6 rounded-lg shadow-md">
                <PlantEnvironmentChart />
            </section>
        </div>
    );
};

export default PlantDashboard;
