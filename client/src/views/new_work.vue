<template>
    <div class="new-work">
      <h1>My Works</h1>
      
      <!-- Done Works Table -->
      <h2>Done Works</h2>
      <table v-if="doneWorks.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Description</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in doneWorks" :key="index">
            <td>{{ work.name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>{{ work.description }}</td>
            <td>{{ work.rating || 'No Rating' }}</td>
          </tr>
        </tbody>
      </table>
  
      <!-- Closed Works Table -->
      <h2>Closed Works</h2>
      <table v-if="closedWorks.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in closedWorks" :key="index">
            <td>{{ work.name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>{{ work.description }}</td>
          </tr>
        </tbody>
      </table>
  
      <!-- Open Works Table -->
      <h2>Open Works</h2>
      <table v-if="openWorks.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in openWorks" :key="index">
            <td>{{ work.name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>{{ work.description }}</td>
            <td>
              <button @click="editWork(work)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- New Work Form -->
      <h2>Create New Work</h2>
      <form @submit.prevent="submitNewWork">
        <input v-model="newWork.name" placeholder="Work Name" required />
        <input v-model="newWork.amount" type="number" placeholder="Amount" required />
        <textarea v-model="newWork.description" placeholder="Description" required></textarea>
        <input v-model="newWork.date" type="date" required />
        <input v-model="newWork.address" placeholder="Address" required />
        
          
          <select id="city" v-model="city" required>
            <option value="" disabled>Select your city</option>
            <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }}</option>
          </select>
        
        <button type="submit">Create Work</button>
      </form>
  
      <!-- Edit Work Form -->
      <div v-if="isEditing">
        <h3>Edit Work</h3>
        <form @submit.prevent="submitEditWork">
          <input v-model="editWork.name" placeholder="Work Name" required />
          <input v-model="editWork.amount" type="number" placeholder="Amount" required />
          <textarea v-model="editWork.description" placeholder="Description" required></textarea>
          <input v-model="editWork.date" type="date" required />
          <input v-model="editWork.address" placeholder="Address" required />
          <input v-model="editWork.city" placeholder="City" required />
          <button type="submit">Update Work</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { useRouter } from 'vue-router';
  export default {
    name: "CustomerNewWork",
    setup() {
      const doneWorks = ref([]);
      const closedWorks = ref([]);
      const openWorks = ref([]);
      const isEditing = ref(false);
      const router = useRouter();
      const newWork = ref({
        name: "",
        description: "",
        amount: null,
        service: "kaam",
        address: "",
        city: "Hyderabad",
        date: "",
      });
  
      // Fetch work data
      onMounted(async () => {
        try {
          const response = await fetch("http://localhost:5000/customer/new_work", {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
          });
          const data = await response.json();
          doneWorks.value = data.done_works;
          closedWorks.value = data.closed_works;
          openWorks.value = data.open_works;
        } catch (error) {
          console.error("Error fetching works data:", error);
          router.push('/login');
        }
      };try {
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
        });
  
      // Edit work
      const editWork = (work) => {
        isEditing.value = true;
        editWork.value = { ...work };
      };
  
      // Submit new work
      const submitNewWork = async () => {
        try {
          const response = await fetch("http://localhost:5000/customer/new_work", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({
              operation: "new",
              ...newWork.value,
            }),
          });
          if (response.ok) {
            alert("New work created successfully!");
            location.reload();
            // Refetch the data
          } else {
            alert("Failed to create new work.");
          }
        } catch (error) {
          console.error("Error creating new work:", error);
        }
      };
  
      // Submit edit work
      const submitEditWork = async () => {
        try {
          const response = await fetch("http://localhost:5000/customer/new_work", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({
              operation: "update",
              ...editWork.value,
            }),
          });
          if (response.ok) {
            alert("Work updated successfully!");
            isEditing.value = false;
          } else {
            alert("Failed to update work.");
          }
        } catch (error) {
          console.error("Error updating work:", error);
        }
      };
  
      return {
        doneWorks,
        closedWorks,
        openWorks,
        newWork,
        editWork,
        isEditing,
        submitNewWork,
        submitEditWork,
        editWork,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Add necessary styles here */
  .new-work {
    margin: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  th, td {
    padding: 10px;
    border: 1px solid #ddd;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  form {
    margin-top: 20px;
  }
  
  input, textarea, select, option {
    display: block;
    margin: 10px 0;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
  }
  
  textarea {
    height: 100px;
  }
  
  button[type="submit"] {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
  }
  
  button[type="submit"]:hover {
    background-color: #45a049;
  }
  </style>
  