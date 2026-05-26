// src/mixins/authMixin.js
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      errorMessage: "",
    };
  },

  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    async login() {
      try {
        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/auth/login",
          {
            email: this.email.trim(),
            password: this.password,
          },
          { withCredentials: true }
        );

        const role = response.data.role?.trim();

        console.log("Logged in role:", role);

        localStorage.setItem("role", role);

        if (role === "Admin") {
          this.$router.push("/admin-dashboard");

        } else if (
          ["Program Chairperson", "Department Chairperson"].includes(role)
        ) {
          this.$router.push("/progchair-dashboard");

        } else if (role === "Faculty") {
          this.$router.push("/faculty-dashboard");

        } else {
          toast.error("Unauthorized role.");
        }

      } catch (error) {
        console.error(error);

        toast.error("Login failed. Please check your credentials.");

        this.errorMessage = "Login failed.";

        setTimeout(() => {
          this.errorMessage = "";
        }, 3000);
      }
    },
  },
};