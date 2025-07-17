// lib/services/auth_service.dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // 1. Enhanced login with email/password + remember me
  Future<User?> signInWithEmailAndPassword(
    String email, 
    String password, {
    bool rememberMe = false,
  }) async {
    try {
      final UserCredential userCredential = 
          await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      // Save credentials if "Remember Me" is checked
      if (rememberMe) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('email', email);
        await prefs.setString('password', password);
      }

      return userCredential.user;
    } on FirebaseAuthException catch (e) {
      throw _authErrorToMessage(e.code);
    } catch (e) {
      throw 'Login failed. Please try again.';
    }
  }

  // 2. Enhanced registration
  Future<User?> registerWithEmailAndPassword(
    String email, 
    String password,
  ) async {
    try {
      final UserCredential userCredential = 
          await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      return userCredential.user;
    } on FirebaseAuthException catch (e) {
      throw _authErrorToMessage(e.code);
    } catch (e) {
      throw 'Registration failed. Please try again.';
    }
  }

  // 3. Password reset
  Future<void> sendPasswordResetEmail(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
    } on FirebaseAuthException catch (e) {
      throw _authErrorToMessage(e.code);
    }
  }

  // 4. Sign out with optional credential clearing
  Future<void> signOut({bool clearCredentials = false}) async {
    await _auth.signOut();
    if (clearCredentials) {
      await clearSavedCredentials();
    }
  }

  // 5. Error message converter
  String _authErrorToMessage(String code) {
    switch (code) {
      case 'invalid-email': return 'Invalid email format';
      case 'user-not-found': return 'No account found';
      case 'wrong-password': return 'Incorrect password';
      case 'user-disabled': return 'Account disabled';
      case 'email-already-in-use': return 'Email already registered';
      case 'weak-password': return 'Password is too weak';
      case 'operation-not-allowed': return 'Operation not allowed';
      default: return 'Authentication failed. Please try again.';
    }
  }

  // 6. Check saved credentials
  Future<Map<String, String>?> getSavedCredentials() async {
    final prefs = await SharedPreferences.getInstance();
    final email = prefs.getString('email');
    final password = prefs.getString('password');
    
    if (email != null && password != null) {
      return {'email': email, 'password': password};
    }
    return null;
  }

  // 7. Clear saved credentials
  Future<void> clearSavedCredentials() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('email');
    await prefs.remove('password');
  }

  // 8. Get current user
  User? getCurrentUser() {
    return _auth.currentUser;
  }
}