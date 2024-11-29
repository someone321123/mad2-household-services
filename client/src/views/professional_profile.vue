<template>
    <div class="profile-container">
      <h1>Professional Profile</h1>
      <div v-if="professional">
        <p><strong>Name:</strong> {{ professional.name }}</p>
        <p><strong>Email:</strong> {{ professional.email }}</p>
        <p><strong>City:</strong> {{ professional.city }}</p>
        <p><strong>Service:</strong> {{ professional.service }}</p>
        <p><strong>Rating:</strong> {{ professional.rating || "Not rated" }}</p>
        <p><strong>Experience:</strong> {{ professional.experience || "No experience listed" }}</p>
  
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
  import { useRouter } from 'vue-router';
  
  export default {
    name: "ProfessionalProfile",
    setup() {
      const professional = ref(null);
      const email = ref("");
      const city = ref("");
      const cities = ref([]);
      const router = useRouter();
  
      // Fetch professional data
      onMounted(async () => {
        try {
          const response = await fetch("http://localhost:5000/professional/profile", {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
          });
  
          if (response.ok) {
            professional.value = await response.json();
            email.value = professional.value.email;
            city.value = professional.value.city;
          } else {
            console.error("Failed to fetch professional profile");
            router.push('/login');
          }
        } catch (error) {
          console.error("Error fetching professional profile:", error);
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
        const updatedData = {
          email: email.value,
          city: city.value,
        };
  
        try {
          const response = await fetch("http://localhost:5000/professional/profile", {
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
        }
      };
  
      return {
        professional,
        email,
        city,
        cities,
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
  