<template>
    <div class="discover-container">
      <h1>Discover</h1>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by work name or customer"
        class="search-input"
      />
      <table class="discover-table">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Customer</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in filteredWorks" :key="index">
            <td>{{ item.name }}</td>
            <td>
              <button @click="showCustomerDetails(item.customer)">
                {{ item.customer.name }}
              </button>
            </td>
            <td>{{ item.amount }}</td>
            <td>{{ formatDate(item.date) }}</td>
            <td>
              <button @click="openOfferForm(item)">Send Offer</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Customer Details Modal -->
      <div v-if="showDetailsModal" class="modal">
        <div class="modal-content">
          <h2>Customer Details</h2>
          <p><strong>Name:</strong> {{ selectedCustomer.name }}</p>
          <p><strong>Email:</strong> {{ selectedCustomer.email }}</p>
          <p><strong>City:</strong> {{ selectedCustomer.city }}</p>
          <p><strong>Work Name:</strong> {{ selectedWork.name }}</p>
          <p><strong>Amount:</strong> {{ selectedWork.amount }}</p>
          <p><strong>Target:</strong> {{ selectedCustomer.id }}</p>
          <p><strong>Date:</strong> {{ formatDate(selectedWork.date) }}</p>
          <button @click="closeCustomerDetails">Close</button>
        </div>
      </div>
  
      <!-- Send Offer Form -->
      <div v-if="showOfferForm" class="modal">
        <div class="modal-content">
          <h2>Send Offer</h2>
          <form @submit.prevent="submitOffer">
            <div class="form-group">
              <label for="work_name">Work Name</label>
              <input type="text" id="work_name" v-model="offer.work_name" required />
            </div>
            <div class="form-group">
              <label for="amount">Amount</label>
              <input type="number" id="amount" v-model="offer.amount" required />
            </div>
            <div class="form-group">
              <label for="date">Date</label>
              <input type="date" id="date" v-model="offer.date" required />
            </div>
            <button type="submit">Submit Offer</button>
            <button type="button" @click="closeOfferForm">Cancel</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from "vue";
  import { useRouter } from "vue-router";
  
  export default {
    name: "DiscoverPage",
    setup() {
      const router = useRouter();
      const works = ref([]);
      const searchQuery = ref("");
      const showDetailsModal = ref(false);
      const showOfferForm = ref(false);
      const selectedCustomer = ref(null);
      const selectedWork = ref(null);
      const offer = ref({
        work_name: "",
        amount: null,
        target: null,
        date: "",
      });
  
      // Fetch works from backend on mount
      onMounted(async () => {
        try {
            const response = await fetch("http://localhost:5000/professional/discover", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
});

if (response.ok) {
  works.value = await response.json();
} else {
  // Check response status for more detailed error handling
  const errorText = await response.text();
  console.error("Failed to fetch works:", response.status, errorText);
  router.push('/login')
  alert('unapproved yet')
}} catch (error) {
          console.error("Error fetching works:", error);
        }
      });
  
      // Format date to yyyy-mm-dd
      const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toISOString().split("T")[0];
      };
  
      // Filter works based on the search query
      const filteredWorks = computed(() => {
        if (!searchQuery.value) return works.value;
        return works.value.filter(
          (work) =>
            work.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            work.customer.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
      });
  
      // Show customer details in a modal
      const showCustomerDetails = (customer) => {
        selectedCustomer.value = customer;
        selectedWork.value = works.value.find(
          (work) => work.customer.id === customer.id
        );
        showDetailsModal.value = true;
      };
  
      // Close the customer details modal
      const closeCustomerDetails = () => {
        showDetailsModal.value = false;
      };
  
      // Open the offer form
      const openOfferForm = (work) => {
        offer.value.work_name = work.name;
        offer.value.target = work.customer.id;
        offer.value.amount = work.amount;
        offer.value.date = formatDate(work.date);
        showOfferForm.value = true;
      };
  
      // Close the offer form
      const closeOfferForm = () => {
        showOfferForm.value = false;
      };
  
      // Submit the offer
      const submitOffer = async () => {
        try {
          const response = await fetch("http://localhost:5000/professional/discover", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify(offer.value),
          });
          if (response.ok) {
            alert("Offer sent successfully!");
            closeOfferForm();
            location.reload();
          } else {
            alert("Failed to send offer");
          }
        } catch (error) {
          console.error("Error submitting offer:", error);
        }
      };
  
      return {
        works,
        searchQuery,
        showDetailsModal,
        showOfferForm,
        selectedCustomer,
        selectedWork,
        offer,
        formatDate,
        filteredWorks,
        showCustomerDetails,
        closeCustomerDetails,
        openOfferForm,
        closeOfferForm,
        submitOffer,
      };
    },
  };
  </script>
  
  <style scoped>
  .discover-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .search-input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .discover-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .discover-table th,
  .discover-table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
  }
  
  button {
    padding: 5px 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  button:disabled {
    background-color: #bbb;
    cursor: not-allowed;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 400px;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  .form-group label {
    display: block;
    font-weight: bold;
  }
  
  .form-group input {
    width: 100%;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button[type="submit"] {
    background-color: #007bff;
  }
  
  button[type="submit"]:hover {
    background-color: #0056b3;
  }
  </style>
