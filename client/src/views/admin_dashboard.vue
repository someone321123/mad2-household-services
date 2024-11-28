<template>
    <div class="statistics-container">
      <h1>Admin Statistics</h1>
      <div v-if="statistics">
        <p><strong>Message:</strong> {{ statistics.message }}</p>
        <p><strong>Number of Customers:</strong> {{ statistics.num_cust }}</p>
        <p><strong>Number of Professionals:</strong> {{ statistics.num_prof }}</p>
        <p><strong>Done Work Offers:</strong> {{ statistics.done_count_work }}</p>
        <p><strong>Not Done Work Offers:</strong> {{ statistics.not_done_count_work }}</p>
  
        <h2>Update Statistics</h2>
        <form @submit.prevent="updateStatistics">
          <div class="form-group">
            <label for="entity">Entity</label>
            <select id="entity" v-model="entity" required>
              <option value="service">Service</option>
              <option value="location">Location</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" v-model="name" required />
          </div>
  
          <div class="form-group">
            <label for="info">Info</label>
            <input type="text" id="info" v-model="info" required />
          </div>
  
          <button type="submit">Update</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  
  export default {
    name: "AdminStatistics",
    setup() {
      const statistics = ref(null);
      const entity = ref("service");
      const name = ref("");
      const info = ref("");
  
      // Fetch admin statistics
      onMounted(async () => {
        try {
          const response = await fetch("http://localhost:5000/admin/statistics", {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
          });
  
          if (response.ok) {
            statistics.value = await response.json();
          } else {
            console.error("Failed to fetch admin statistics");
          }
        } catch (error) {
          console.error("Error fetching admin statistics:", error);
        }
      });
  
      // Handle form submission
      const updateStatistics = async () => {
        const data = {
          entity: entity.value,
          name: name.value,
          info: info.value,
        };
  
        try {
          const response = await fetch("http://localhost:5000/admin/statistics", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify(data),
          });
  
          if (response.ok) {
            alert("Statistics updated successfully!");
          } else {
            alert("Failed to update statistics.");
          }
        } catch (error) {
          console.error("Error updating statistics:", error);
        }
      };
  
      return {
        statistics,
        entity,
        name,
        info,
        updateStatistics,
      };
    },
  };
  </script>
  
  <style scoped>
  .statistics-container {
    padding: 20px;
    max-width: 800px;
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
  