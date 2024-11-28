<template>
    <div class="profile-container">
      <h1>Customer Profile</h1>
      <div v-if="customer">
        <p><strong>Name:</strong> {{ customer.name }}</p>
        <p><strong>Email:</strong> {{ customer.email }}</p>
        <p><strong>City:</strong> {{ customer.city }}</p>
        <p><strong>Role:</strong> {{ customer.role }}</p>
  
        <h2>Update Profile</h2>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required />
          </div>
  
          <div class="form-group">
            <label for="city">City</label>
            <select id="city" v-model="city" required>
              <option v-for="city in cities" :key="city.id" :value="city.name">
                {{ city.name }}
              </option>
            </select>
          </div>
  
          <button type="submit">Update</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  
  export default {
    name: "CustomerProfile",
    setup() {
      const customer = ref(null);
      const email = ref("");
      const city = ref("");
      const cities = ref([]);
      const loading = ref(false);
  
      // Fetch customer data
      onMounted(async () => {
        try {
          const response = await fetch("http://localhost:5000/customer/profile", {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
          });
  
          if (response.ok) {
            customer.value = await response.json();
            email.value = customer.value.email;
            city.value = customer.value.city;
          } else {
            console.error("Failed to fetch customer profile");
          }
        } catch (error) {
          console.error("Error fetching customer profile:", error);
        }
  
        // Fetch cities
        try {
          const cityResponse = await fetch("http://localhost:5000/hello_world");
          if (cityResponse.ok) {
            const data = await cityResponse.json();
            cities.value = data.cities;
          } else {
            console.error("Failed to fetch cities");
          }
        } catch (error) {
          console.error("Error fetching cities:", error);
        }
      });
  
      // Handle form submission
      const updateProfile = async () => {
        loading.value = true;
        const updatedData = {
          email: email.value,
          city: city.value,
        };
  
        try {
          const response = await fetch("http://localhost:5000/customer/profile", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify(updatedData),
          });
  
          if (response.ok) {
            alert("Profile updated successfully!");
          } else {
            alert("Failed to update profile.");
          }
        } catch (error) {
          console.error("Error updating profile:", error);
        } finally {
          loading.value = false;
        }
      };
  
      return {
        customer,
        email,
        city,
        cities,
        loading,
        updateProfile,
      };
    },
  };
  </script>
  
  <style scoped>
  .profile-container {
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
  }
  
  form {
    margin-top: 20px;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  button {
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
  }
  
  button:disabled {
    background-color: #ccc;
  }
  </style>
  