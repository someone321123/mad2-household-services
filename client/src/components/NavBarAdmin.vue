<!-- src/components/NavBarAdmin.vue -->
<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li class="navbar-item"><router-link to="/admin_dashboard">WELCOME ADMIN</router-link></li>
      <li class="navbar-item"><router-link to="/admin_dashboard">Dashboard</router-link></li>
      <li class="navbar-item"><router-link to="/administrator">Administrator</router-link></li>
      <li class="navbar-item"><button @click="exportCSV">Export CSV</button></li>
      <li class="navbar-item"><button class="logout" @click="logout">Logout</button></li>
    </ul>
  </nav>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default {
  setup() {
    const router = useRouter();

    const exportCSV = async () => {
      try {
        const response = await fetch("http://localhost:5000/admin/backend", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
          // Remove body for GET request
        });
  
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'export.csv';
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url); 
          
          alert("Export successful!");
        } else {
          const errorText = await response.text();
          alert(`Export failed: ${errorText}`);
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred during export");
      }
    };

    const logout = () => {
      localStorage.clear();
      router.push('/login').then(() => {
        router.go(0);
      });
    };

    return {
      logout,
      exportCSV
    };
  }
}
</script>
<style scoped>
.navbar {
background-color: #008000; /* Green background */

top: 0;
width: 100%;
height: 50px; /* Fixed height */
}

.navbar-list {
list-style-type: none;
margin: 0;
padding: 0;
display: flex; /* Use flexbox for horizontal layout */
justify-content: center; /* Center items horizontally */
align-items: center; /* Center items vertically */
height: 100%; /* Full height of navbar */
}

.navbar-item {
margin: 0 10px; /* Space between items */
}

.navbar-item a, .navbar-item button {
color: white;
text-decoration: none;
background: none;
border: none;
cursor: pointer;
padding: 10px 15px;
transition: background-color 0.3s ease;
}

.navbar-item a:hover, .navbar-item button.logout:hover {
background-color: rgba(255, 255, 255, 0.2); /* Subtle hover effect */
color: white;
}

.navbar-item button{
font-size: inherit;
font-family: inherit;
}
</style>
    