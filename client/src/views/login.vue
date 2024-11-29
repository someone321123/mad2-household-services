<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" id="name" v-model="name" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" :disabled="loading">Login</button> 
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'LoginPage',
    setup() {
      const router = useRouter();
      const name = ref('');
      const password = ref('');
      const loading = ref(false);
      const errorMessage = ref('');
  
      const handleLogin = async () => {
        loading.value = true;
        errorMessage.value = ''; 
  
        try {
          const response = await fetch('http://localhost:5000/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: name.value,
              password: password.value,
            }),
          });
  
          if (!response.ok) {
            throw new Error('Login failed');
          }
  
          const data = await response.json();
  
          // Store token and role in localStorage
          localStorage.setItem('token', data.access_token.toString());
          localStorage.setItem('role', data.role);
  
          // Navigate based on user role
          switch(data.role) {
  case 'admin':
    router.push({ name: 'admin_dashboard' }).then(() => {
      router.go(0); // Recommended Vue Router method for full page reload
    });
    break;
  case 'customer':
    router.push({ name: 'new_work' }).then(() => {
      router.go(0);
    });
    break;
  case 'professional':
    router.push({ name: 'discover' }).then(() => {
      router.go(0);
    });
    break;
  default:
    router.push({ name: 'login' });
}
        } catch (error) {
          errorMessage.value = error.message || 'Login failed';
        } finally {
          loading.value = false;
        }
      };
  
      return {
        name,
        password,
        loading,
        errorMessage,
        handleLogin,
      };
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
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
  }
  
  .error {
    color: red;
    font-size: 14px;
    margin-top: 10px;
  }
  </style>
  
  