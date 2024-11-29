<template>
    <div class="admin-dashboard">
      <h1>Admin Dashboard</h1>
      
      <!-- Approved Professionals Table -->
      <h2>Approved Professionals</h2>
      <table v-if="approved.length">
        <thead>
          <tr>
            <th>Name</th>
            <th>City</th>
            <th>Email</th>
            <th>Service</th>
            <th>Rating</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prof, index) in approved" :key="index">
            <td>{{ prof.name }}</td>
            <td>{{ prof.city }}</td>
            <td>{{ prof.email }}</td>
            <td>{{ prof.service }}</td>
            <td>{{ prof.rating || 'No Rating' }}</td>
            <td>
              <button @click="unapproveProfessional(prof.id)">Unapprove</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Unapproved Professionals Table -->
      <h2>Unapproved Professionals</h2>
      <table v-if="unapproved.length">
        <thead>
          <tr>
            <th>Name</th>
            <th>City</th>
            <th>Email</th>
            <th>Service</th>
            <th>Rating</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prof, index) in unapproved" :key="index">
            <td>{{ prof.name }}</td>
            <td>{{ prof.city }}</td>
            <td>{{ prof.email || 'Not Provided' }}</td>
            <td>{{ prof.service }}</td>
            <td>{{ prof.rating || 'No Rating' }}</td>
            <td>
              <button @click="approveProfessional(prof.id)">Approve</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { useRouter } from 'vue-router';
  export default {
    name: "AdminDashboard",
    setup() {
      const approved = ref([]);
      const unapproved = ref([]);
      const router = useRouter();
      // Fetch approved and unapproved professionals
      onMounted(async () => {
        try {
          const response = await fetch("http://localhost:5000/admin/dashboard", {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
          }); if (!response.ok){router.push('/login');}
          const data = await response.json();
          approved.value = data.approved;
          unapproved.value = data.unapproved;
        } catch (error) {
          console.error("Error fetching dashboard data:", error);
          router.push('/login');
        }
      });
  
      // Approve a professional
      const approveProfessional = async (professionalId) => {
        try {
          const response = await fetch("http://localhost:5000/admin/dashboard", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({
              professional_id: professionalId,
              approval: "T",
            }),
          });
          if (response.ok) {
            alert("Professional approved successfully");
            location.reload();
            // Refetch or update the data here
          } else {
            alert("Failed to approve professional.");
          }
        } catch (error) {
          console.error("Error approving professional:", error);
        }
      };
  
      // Unapprove a professional
      const unapproveProfessional = async (professionalId) => {
        try {
          const response = await fetch("http://localhost:5000/admin/dashboard", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({
              professional_id: professionalId,
              approval: "F",
            }),
          });
          if (response.ok) {
            alert("Professional unapproved successfully");
            location.reload();
            // Refetch or update the data here
          } else {
            alert("Failed to unapprove professional.");
          }
        } catch (error) {
          console.error("Error unapproving professional:", error);
        }
      };
  
      return {
        approved,
        unapproved,
        approveProfessional,
        unapproveProfessional,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Add necessary styles here */
  .admin-dashboard {
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
  </style>
  