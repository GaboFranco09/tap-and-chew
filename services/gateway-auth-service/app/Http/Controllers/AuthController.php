<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Facades\Validator;
use Tymon\JWTAuth\Facades\JWTAuth;

class AuthController extends Controller
{
    // ─── REGISTER ────────────────────────────────────────────────

    public function register(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name'     => 'required|string|max:255',
            'email'    => 'required|email|unique:users',
            'password' => 'required|string|min:8|confirmed',
            'role'     => 'sometimes|in:admin,cashier,kitchen,customer',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $user = User::create([
            'name'     => $request->name,
            'email'    => $request->email,
            'password' => Hash::make($request->password),
            'role'     => $request->role ?? 'customer',
        ]);

        $token = JWTAuth::fromUser($user);

        return response()->json([
            'message' => 'Registro exitoso.',
            'user'    => $this->userResponse($user),
            'token'   => $token,
        ], 201);
    }

    // ─── LOGIN ───────────────────────────────────────────────────

    public function login(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email'    => 'required|email',
            'password' => 'required|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $user = User::where('email', $request->email)->first();

        if (! $user || ! Hash::check($request->password, $user->password)) {
            return response()->json(['message' => 'Credenciales inválidas.'], 401);
        }

        if (! $user->is_active) {
            return response()->json(['message' => 'Cuenta desactivada.'], 403);
        }

        $token = JWTAuth::fromUser($user);

        return response()->json([
            'message' => 'Login exitoso.',
            'user'    => $this->userResponse($user),
            'token'   => $token,
        ]);
    }

    // ─── LOGOUT ──────────────────────────────────────────────────

    public function logout()
    {
        JWTAuth::invalidate(JWTAuth::getToken());

        return response()->json(['message' => 'Sesión cerrada exitosamente.']);
    }

    // ─── ME ──────────────────────────────────────────────────────

    public function me()
    {
        $user = JWTAuth::parseToken()->authenticate();

        return response()->json($this->userResponse($user));
    }

    // ─── FORGOT PASSWORD ─────────────────────────────────────────

    public function forgotPassword(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email' => 'required|email',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        Password::sendResetLink($request->only('email'));

        return response()->json([
            'message' => 'Si el correo existe, recibirás un enlace de recuperación.',
        ]);
    }

    // ─── RESET PASSWORD ──────────────────────────────────────────

    public function resetPassword(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'token'    => 'required',
            'email'    => 'required|email',
            'password' => 'required|string|min:8|confirmed',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function (User $user, string $password) {
                $user->forceFill(['password' => Hash::make($password)])->save();
            }
        );

        if ($status !== Password::PASSWORD_RESET) {
            return response()->json(['message' => 'Token inválido o expirado.'], 400);
        }

        return response()->json(['message' => 'Contraseña restablecida exitosamente.']);
    }

    // ─── HELPER ──────────────────────────────────────────────────

    private function userResponse(User $user): array
    {
        return [
            'id'    => $user->id,
            'name'  => $user->name,
            'email' => $user->email,
            'role'  => $user->role,
        ];
    }
}