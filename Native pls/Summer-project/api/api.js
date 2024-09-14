import axios from 'axios';


let user = '66d36a9d42d9a5784e1a59fe';
export const api = axios.create({
    baseURL: 'http://10.11.50.21:5000',
    headers: {
        'Content-Type': 'application/json',
    },
    });

export const getPeople = async () => {
    const response = await api.get(`/people/${user}`);
    return response;
}

export const getHistory = async () => {
    const response = await api.get(`/history/${user}`);
    return response;
}