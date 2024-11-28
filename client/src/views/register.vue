<template>
    <div class="register-container">
      <h1>Register</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>
  
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" id="name" v-model="name" required />
        </div>
  
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
  
        <div class="form-group">
          <label for="city">City</label>
          <select id="city" v-model="city" required>
            <option value="" disabled>Select your city</option>
            <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }}</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="professional">Are you a professional?</label>
          <input type="checkbox" id="professional" v-model="isProfessional" />
        </div>
  
        <!-- Dynamic service dropdown when 'Professional' checkbox is checked -->
        <div v-if="isProfessional" class="form-group">
          <label for="service">Select Service</label>
          <select id="service" v-model="service">
            <option value="" disabled>Select a service</option>
            <option v-for="service in services" :key="service.id" :value="service.name">{{ service.name }}</option>
          </select>
        </div>
  
        <button type="submit" :disabled="loading">Register</button>
  
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  
  export default {
    name: 'RegisterPage',
    setup() {
      const email = ref('');
      const name = ref('');
      const password = ref('');
      const city = ref('');
      const isProfessional = ref(false);
      const service = ref('');
      const cities = ref([]);
      const services = ref([]);
      const errorMessage = ref('');
      const loading = ref(false);
  
      // Fetch cities and services data from /hello_world
      onMounted(async () => {
        try {
          const response = await fetch('http://localhost:5000/hello_world');
          if (response.ok) {
            const data = await response.json();
            cities.value = data.cities;
            services.value = data.services;
          } else {
            console.error('Failed to fetch cities and services');
          }
        } catch (error) {
          console.error('Error fetching cities and services:', error);
        }
      });
  
      const handleRegister = async () => {
        loading.value = true;
        errorMessage.value = ''; // Reset error message
  
        const registrationData = {
          name: name.value,
          password: password.value,
          city: city.value,
          service: isProfessional.value ? service.value : null, // Only include service if user is a professional
        };
  
        try {
          const response = await fetch('http://localhost:5000/auth/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(registrationData),
          });
  
          if (!response.ok) {
            throw new Error('Registration failed');
          }
  
          alert('Registration successful!');
          // Redirect or reset form after successful registration (optional)
          // router.push({ name: 'login' }); // Example: redirect to login page after registration
        } catch (error) {
          errorMessage.value = error.message || 'An error occurred during registration';
        } finally {
          loading.value = false;
        }
      };
  
      return {
        email,
        name,
        password,
        city,
        isProfessional,
        service,
        cities,
        services,
        errorMessage,
        loading,
        handleRegister,
      };
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
  }
  
  input,
  select {
    width: 100%;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  button:disabled {
    background-color: #bbb;
    cursor: not-allowed;
  }
  
  .error {
    color: red;
    font-size: 14px;
    margin-top: 10px;
  }
  </style>
  
  
  