import React, { useState, useEffect } from 'react';
import PlantRecordCard from '../components/PlantRecordCard';

const backendIP = process.env.REACT_APP_BACKEND_IP;

function History() {
    const [records, setRecords] = useState([]);

    useEffect(() => {
        async function fetchPlantRecords() {
            try {
                const response = await fetch(
                    `${backendIP}api/plant/get-plant/`
                );
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setRecords(data);
            } catch (error) {
                console.error('Error fetching plant records:', error);
            }
        }

        fetchPlantRecords();
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
            <h1 className="text-3xl font-bold mb-6">식물 기록</h1>
            <div className="w-full max-w-2xl">
                {records
                    .slice()
                    .reverse()
                    .map((record, index) => (
                        <PlantRecordCard key={index} record={record} />
                    ))}
            </div>
        </div>
    );
}

export default History;
