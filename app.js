const client = new Appwrite.Client()
  .setEndpoint('https://cloud.appwrite.io/v1')
  .setProject('68828618001920a46bd8');

const account = new Appwrite.Account(client);

const form = document.getElementById('loginForm');
const statusDiv = document.getElementById('status');

// Validate email and password
function validateInputs(email, password) {
  if (!email || !password) {
    statusDiv.textContent = '❌ Please fill in all fields';
    return false;
  }
  if (password.length < 8) {
    statusDiv.textContent = '❌ Password must be at least 8 characters';
    return false;
  }
  return true;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = form.email.value.trim();
  const password = form.password.value;

  if (!validateInputs(email, password)) return;

  statusDiv.textContent = 'Logging in...';

  try {
    const session = await account.createEmailSession(email, password);
    statusDiv.textContent = `✅ Logged in! Welcome ${email}`;
    console.log('Session created:', session);
  } catch (err) {
    statusDiv.textContent = `❌ Login failed: ${err.message}`;
    console.error('Login error:', err);
  }
});

document.getElementById('registerBtn').addEventListener('click', async () => {
  const email = form.email.value.trim();
  const password = form.password.value;

  if (!validateInputs(email, password)) return;

  statusDiv.textContent = 'Registering...';

  try {
    // Create user account
    const user = await account.create('unique()', email, password);
    statusDiv.textContent = '✅ Registered! Now logging in...';
    console.log('User created:', user);

    // Auto-login after registration
    const session = await account.createEmailSession(email, password);
    statusDiv.textContent = `✅ Registered & logged in as ${email}`;
    console.log('Session created:', session);
  } catch (err) {
    // More detailed error handling
    if (err.code === 409) {
      statusDiv.textContent = '❌ Email already registered. Try logging in instead.';
    } else if (err.message.includes('fetch')) {
      statusDiv.textContent = '❌ Connection error. Check CORS settings in Appwrite Console.';
    } else {
      statusDiv.textContent = `❌ Registration failed: ${err.message}`;
    }
    console.error('Registration error:', err);
  }
});