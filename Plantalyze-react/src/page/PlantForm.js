import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import PlantImageUpload from '../components/PlantImageUpload';
import NumberInputWithButtons from '../components/NumberInputWithButtons';
import Spinner from '../components/Spinner';

const backendIP = process.env.REACT_APP_BACKEND_IP;

function PlantForm() {
    const [file, setFile] = useState(null);
    const navigate = useNavigate(); // useHistory 훅 사용
    const [waterAmount, setWaterAmount] = useState(0);
    const [sunlightHours, setSunlightHours] = useState(0);
    const [windHours, setWindHours] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true); // 로딩 상태 활성화
        try {
            const formData = new FormData();
            formData.append('image', file); // 파일 추가
            formData.append('skip_processing', true);
            formData.append('bbox_left_top_x', waterAmount);
            formData.append('bbox_left_top_y', sunlightHours);
            formData.append('bbox_right_bottom_x', windHours);

            const response = await axios.post(
                `${backendIP}api/plant/create/`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            setIsLoading(false);
            navigate('/dashboard'); // 성공 페이지로 이동

            console.log('API 응답:', response.data);
        } catch (error) {
            setIsLoading(false);
            alert('실패');
            console.error('API 호출 오류:', error);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
            {/* 배경에 불투명한 배경을 추가하여 다른 요소를 클릭하지 못하도록 함 */}
            {isLoading && (
                <div className="fixed inset-0 bg-black opacity-50 z-50"></div>
            )}
            <form
                onSubmit={handleSubmit}
                className="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg"
            >
                <h2 className="text-2xl font-bold mb-4">식물 정보 전송</h2>
                <PlantImageUpload externalFile={file} onFileChange={setFile} />
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                        물 주기 (ml, 하루단위)
                    </label>
                    <NumberInputWithButtons
                        value={waterAmount}
                        onChange={setWaterAmount}
                        step={100}
                        min={0}
                        max={5000}
                        name="bbox_left_top_x"
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                        조명 (시간, 하루단위)
                    </label>
                    <NumberInputWithButtons
                        value={sunlightHours}
                        onChange={setSunlightHours}
                        step={1}
                        min={0}
                        max={50}
                        name="example"
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                        바람 (시간, 하루단위)
                    </label>
                    <NumberInputWithButtons
                        value={windHours}
                        onChange={setWindHours}
                        step={1}
                        min={0}
                        max={50}
                        name="example"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full py-2 px-4 bg-blue-500 text-white font-bold rounded-md hover:bg-blue-600"
                >
                    {isLoading ? '제출 중...' : '제출'}
                </button>
                {isLoading && (
                    <Spinner className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                )}{' '}
                {/* 로딩 상태 표시 */}
            </form>
        </div>
    );
}

export default PlantForm;
