import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://49.247.196.148:8080/api',
});