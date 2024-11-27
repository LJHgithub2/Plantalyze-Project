// Header.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
    const location = useLocation();

    const linkClasses = (path) =>
        `text-gray-600 hover:text-blue-500 transition-colors duration-300 ${
            location.pathname === path
                ? 'text-blue-600 border-b-2 border-blue-600'
                : ''
        }`;

    return (
        <header className="bg-gradient-to-r from-green-100 via-white to-green-100 w-full py-5 flex-col justify-center">
            <h1 className="text-3xl font-bold text-center text-gray-800">
                식물 키우기
            </h1>
            <nav className="mt-4">
                <ul className="flex justify-center space-x-8">
                    <li>
                        <Link to="/history" className={linkClasses('/history')}>
                            History
                        </Link>
                    </li>
                    <li>
                        <Link
                            to="/dashboard"
                            className={linkClasses('/dashboard')}
                        >
                            DashBoard
                        </Link>
                    </li>
                    <li>
                        <Link to="/update" className={linkClasses('/update')}>
                            Update
                        </Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
