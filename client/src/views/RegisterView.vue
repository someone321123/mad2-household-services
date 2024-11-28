<template>
  <form class="mx-auto mt-5 w-50" @submit.prevent="submitForm">
    
    <div class="mb-3">
      <label for="name" class="form-label fw-bold">Username</label>
      <input type="text" class="form-control" id="name" v-model="form.name" >
    </div>
    <div class="mb-3">
      <label for="password" class="form-label fw-bold">Password</label>
      <input type="password" class="form-control" v-model="form.password" id="password">
    </div>
    <div class="mb-3">
      <label for="city" class="form-label fw-bold">City</label>
      <input type="text" class="form-control" v-model="form.city" id="city">
      
    </div>


    <div>
        <label>
          <input type="checkbox" v-model="isProfessional" />
          Are you a professional?
        </label>
      </div>
      <div v-if="isProfessional">
        <label for="service">Service Type</label>
        <input 
          type="text" 
          id="service" 
          v-model="form.service" 
          placeholder="Enter your service type"
          required
        />
      </div>



    
    <button type="submit" class="btn btn-dark">Submit</button>
  </form>
</template>
<script>
export default {
  name: "Register",
  data() {
    return {
      form: {
        name: "",
        password: "",
        city: "",
        service: "",
      },
      isProfessional: false,
    };
  },
  methods: {
    async submitForm() {
      try {
        // Prepare the payload
        const payload = {
          name: this.form.name,
          password: this.form.password,
          city: this.form.city,
        };

        if (this.isProfessional) {
          payload.service = this.form.service;
        }

        // Send the data to the Flask backend
        const response = await fetch("http://127.0.0.1:5000/auth/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }

        const data = await response.json(); // Parse JSON response
        console.log(data);
        localStorage.setItem('token', data.token); // Store token in localStorage
        if (response.ok) {this.$router.push({ name: 'Login' })}

        // Handle success
        alert("Registration successful!");
      } catch (error) {
        alert("An error occurred: " + error.message);
      }
    },
  },
};
</script>


<style scoped></style>