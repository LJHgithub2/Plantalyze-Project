import React from 'react';

function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

function PlantRecordCard({ record }) {
    return (
        <div className="flex-col items-center bg-white shadow-lg rounded-lg overflow-hidden mb-6">
            <div className="p-4 w-full">
                <h2 className="text-2xl font-bold mb-2">{record.plantType}</h2>
                <div className="flex justify-center mb-4">
                    <img
                        src={
                            record.image
                                ? record.image
                                : 'https://via.placeholder.com/300x200.png?text=Plant+Image'
                        }
                        alt={`${record.plantType} 이미지`}
                        className="max-h-64 object-cover"
                    />
                </div>
                <hr className="my-5"></hr>
                <p className="text-gray-700 mb-2">
                    예측 질병: {record.predicted_disease}
                </p>
                <p className="text-gray-700 mb-2">
                    상태 위험도: {record.risk_level}
                </p>
                <p className="text-gray-700 mb-2">
                    현재 상태: {record.current_status}
                </p>
                <p className="text-gray-700 mb-2">
                    개선방안: {record.improvement_plan}
                </p>
                <p className="text-gray-500 text-sm">
                    날짜: {formatDate(record.created_at)}
                </p>
            </div>
        </div>
    );
}

export default PlantRecordCard;
