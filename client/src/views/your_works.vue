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
            <button @click="acceptOffer(work.offer_id, work.amount, new Date(work.date).toLocaleDateString())">Accept</button>
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

    <!-- Professional Details Modal -->
    <div v-if="selectedProfessional" class="modal">
      <div class="modal-content">
        <span class="close" @click="selectedProfessional = null">&times;</span>
        <h2>Professional Details</h2>
        <p><strong>Name:</strong> {{ selectedProfessional.name }}</p>
        <p><strong>Email:</strong> {{ selectedProfessional.email }}</p>
        <p><strong>City:</strong> {{ selectedProfessional.city }}</p>
      </div>
    </div>


    <!-- Negotiate Offer Modal -->
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
      sent: [],
    });

    const router = useRouter();
    const selectedProfessional = ref(null);
    const isNegotiating = ref(false);
    const negotiation = ref({
      amount: 0,
      date: "",
      target: null,
      work_name: null,
    });
    const work = ref(null);


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
            sent: data.sent || [],
          };
        } else {
          console.error("Failed to fetch works data");
          router.push('/login');
        }
      } catch (error) {
        console.error("Error fetching works data:", error);
      }
    });

    const showProfessionalDetails = (professional) => {
      selectedProfessional.value = professional;
    };

    const handleAcceptOffer = async (offerId, od_amount, od_date) => {
      try {
        if (!od_amount || !od_date) {
          alert('Please provide amount and date for accepting the offer');
          return;
        }

        const response = await fetch("http://localhost:5000/professional/your_work", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            offer_id: offerId,
            operation: "accept",
            od_amount: od_amount,
            od_date: od_date
          }),
        });

        if (response.ok) {
          alert("Offer accepted successfully");
          location.reload();
        } else {
          const errorText = await response.text();
          alert(`Failed to accept offer: ${errorText}`);
        }
      } catch (error) {
        console.error("Error accepting offer:", error);
        alert("An error occurred while accepting the offer.");
      }
    };

   

    const handleOfferAction = async (offerId, operation) => {
      try {
        const response = await fetch("http://localhost:5000/professional/your_work", {
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
          alert(`${operation} successful`);location.reload();
        } else {
          const errorText = await response.text();
          alert(`Failed to update offer: ${errorText}`);
        }
      } catch (error) {
        console.error("Error handling offer action:", error);
        alert("An error occurred while processing the offer.");
      }
    };

    const acceptOffer = async (offerId, od_amount, od_date) => {
      await handleAcceptOffer(offerId, od_amount, od_date);
    };

    const rejectOffer = async (offerId) => {
      await handleOfferAction(offerId, "reject");
    };

    const rejectSentOffer = async (offerId) => {
      await handleOfferAction(offerId, "reject");
    };

    const abandonOffer = async (offerId) => {
      await handleOfferAction(offerId, "abandon");
    };

    const negotiateOffer = (work) => {
      negotiation.value = {
        amount: work.amount,
        date: new Date().toISOString().split('T')[0],
        customer_id: work.customer.id,
        offer_id: work.work_name,
      };
      isNegotiating.value = true;
    };

    const submitNegotiation = async () => {
      try {
        const response = await fetch("http://localhost:5000/professional/discover", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            work_name: negotiation.value.offer_id,
            target: negotiation.value.customer_id,
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
      acceptOffer,
      work,
    };
  },
};
</script>

  
  <style scoped>
 
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