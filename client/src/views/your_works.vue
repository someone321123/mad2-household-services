<template>
    <div class="my-works">
      <h1>My Work</h1>
      
      <!-- Active Offers Table -->
      <h2>Active Offers</h2>
      <table v-if="works.active.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Customer</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in works.active" :key="index">
            <td>{{ work.work_name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>
              <button @click="showProfessionalDetails(work.customer)">
                {{ work.customer.name }}
              </button>
            </td>
            <td>
              <button @click="abandonOffer(work.offer_id)">Abandon</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- History Offers Table -->
      <h2>History</h2>
      <table v-if="works.history.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Customer</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in works.history" :key="index">
            <td>{{ work.work_name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>
              <button @click="showProfessionalDetails(work.customer)">
                {{ work.customer.name }}
              </button>
            </td>
            <td>{{ work.rating || 'No rating' }}</td>
          </tr>
        </tbody>
      </table>
  
      <!-- Received Offers Table -->
      <h2>Received Offers</h2>
      <table v-if="works.received.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Customer</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in works.received" :key="index">
            <td>{{ work.work_name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>
              <button @click="showProfessionalDetails(work.customer)">
                {{ work.customer.name }}
              </button>
            </td>
            <td>
              <button @click="acceptOffer(work.offer_id)">Accept</button>
              <button @click="rejectOffer(work.offer_id)">Reject</button>
              <button @click="negotiateOffer(work)">Negotiate</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Sent Offers Table -->
      <h2>Sent Offers</h2>
      <table v-if="works.sent.length">
        <thead>
          <tr>
            <th>Work Name</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Customer</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(work, index) in works.sent" :key="index">
            <td>{{ work.work_name }}</td>
            <td>{{ work.amount }}</td>
            <td>{{ new Date(work.date).toLocaleDateString() }}</td>
            <td>
              <button @click="showProfessionalDetails(work.customer)">
                {{ work.customer.name }}
              </button>
            </td>
            <td>
              <button @click="rejectSentOffer(work.offer_id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Customer Details Modal -->
      <div v-if="selectedProfessional" class="modal">
        <div class="modal-content">
          <span class="close" @click="selectedProfessional = null">&times;</span>
          <h2>Customer Details</h2>
          <p><strong>Name:</strong> {{ selectedProfessional.name }}</p>
          <p><strong>Email:</strong> {{ selectedProfessional.email }}</p>
          <p><strong>City:</strong> {{ selectedProfessional.city }}</p>
          <p><strong>Experience:</strong> {{ selectedProfessional.experience || 'N/A' }}</p>
          <p><strong>Service:</strong> {{ selectedProfessional.service }}</p>
          <p><strong>Rating:</strong> {{ selectedProfessional.rating || 'No rating' }}</p>
        </div>
      </div>
  
      <!-- Negotiate Offer Form -->
      <div v-if="isNegotiating" class="modal">
        <div class="modal-content">
          <span class="close" @click="isNegotiating = false">&times;</span>
          <h2>Negotiate Offer</h2>
          <form @submit.prevent="submitNegotiation">
            <div class="form-group">
              <label for="amount">Amount</label>
              <input type="number" v-model="negotiation.amount" required />
            </div>
            <div class="form-group">
              <label for="date">Date</label>
              <input type="date" v-model="negotiation.date" required />
            </div>
            <button type="submit">Submit Negotiation</button>
          </form>
        </div>
      </div>
    </div>
  </template>
///////////////////////////////////

<script>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
export default {
  name: "MyWork",
  setup() {
    const works = ref({
      active: [],
      history: [],
      received: [],
      sent: [], // Ensure sent offers are initialized
    });
    const router = useRouter();
    const selectedProfessional = ref(null);
    const isNegotiating = ref(false);
    const negotiation = ref({
      amount: 0,
      date: "",
      professional_id: null, // Add professional ID field
      offer_id: null, // Add offer ID field
    });

    // Fetch data for my work
    onMounted(async () => {
      try {
        const response = await fetch("http://localhost:5000/professional/your_work", {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`, // Corrected token key
          },
        });
        
        if (response.ok) {
          const data = await response.json();
          works.value = {
            active: data.active || [],
            history: data.history || [],
            received: data.received || [],
            sent: data.sent || [], // Ensure sent offers are populated
          };
        } else {
          console.error("Failed to fetch works data");
          router.push('/login');
        }
      } catch (error) {
        console.error("Error fetching works data:", error);
      }
    });

    // Show Customer Details
    const showProfessionalDetails = (professional) => {
      selectedProfessional.value = professional;
    };

    // Handle offer actions (Accept/Reject/Abandon)
    const handleOfferAction = async (offerId, operation) => {
      try {
        const response = await fetch("http://localhost:5000/customer/my_work/update", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            offer_id: offerId,
            operation: operation,
          }),
        });

        if (response.ok) {
          alert(`${operation} successful`);
          // Refetch data to update the view
          await onMounted();
        } else {
          const errorText = await response.text();
          alert(`Failed to update offer: ${errorText}`);
        }
      } catch (error) {
        console.error("Error handling offer action:", error);
        alert("An error occurred while processing the offer.");
      }
    };

    // Accept Offer
    const acceptOffer = async (offerId) => {
      await handleOfferAction(offerId, "accept");
    };

    // Reject Offer
    const rejectOffer = async (offerId) => {
      await handleOfferAction(offerId, "reject");
    };

    // Reject Sent Offer
    const rejectSentOffer = async (offerId) => {
      await handleOfferAction(offerId, "reject");
    };

    // Abandon Offer
    const abandonOffer = async (offerId) => {
      await handleOfferAction(offerId, "abandon");
    };

    // Negotiate Offer
    const negotiateOffer = (work) => {
      negotiation.value = {
        amount: work.amount,
        date: new Date().toISOString().split('T')[0],
        professional_id: work.customer.id, // Set professional ID
        offer_id: work.offer_id, // Set offer ID
      };
      isNegotiating.value = true;
    };

    // Submit Negotiation
    const submitNegotiation = async () => {
      try {
        const response = await fetch("http://localhost:5000/professional/your_work", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            offer_id: negotiation.value.offer_id,
            professional_id: negotiation.value.professional_id,
            amount: negotiation.value.amount,
            date: negotiation.value.date,
          }),
        });

        if (response.ok) {
          alert("Negotiation submitted successfully");
          isNegotiating.value = false;
          // Refetch data to update the view
          await onMounted();
        } else {
          const errorText = await response.text();
          alert(`Failed to negotiate offer: ${errorText}`);
        }
      } catch (error) {
        console.error("Error submitting negotiation:", error);
        alert("An error occurred while submitting negotiation.");
      }
    };

    return {
      works,
      selectedProfessional,
      isNegotiating,
      negotiation,
      showProfessionalDetails,
      acceptOffer,
      rejectOffer,
      rejectSentOffer,
      abandonOffer,
      negotiateOffer,
      submitNegotiation,
    };
  },
};
</script>
  
  <style scoped>
  /* Add necessary styles here */
  .my-works {
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
    border-radius: 5px;
    max-width: 500px;
    width: 100%;
  }
  
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 30px;
    font-weight: bold;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  </style> 