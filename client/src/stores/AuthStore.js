import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  
  state: () => ({
    token: null,
    role: null,
    
  }),
  actions: {
    
    async register(userData) {
      try {
        const response = await fetch('http://127.0.0.1:5000/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });
        if (!response.ok) {
          throw new Error('Registration failed');
        }
        return await response.json();
      } catch (error) {
        console.error('Registration error:', error.message);
        throw error;
      }
    },
    logout() { },
  },
});