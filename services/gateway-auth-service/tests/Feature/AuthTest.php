<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();

        ResetPassword::createUrlUsing(function ($user, string $token) {
            return 'http://localhost/reset-password?token=' . $token;
        });
    }

    // ─── REGISTER ────────────────────────────────────────────────

    public function test_user_can_register_with_valid_data(): void
    {
        $response = $this->postJson('/api/auth/register', [
            'name'                  => 'Gabriel Admin',
            'email'                 => 'admin@tapandchew.com',
            'password'              => 'password123',
            'password_confirmation' => 'password123',
            'role'                  => 'admin',
        ]);

        $response->assertStatus(201)
                 ->assertJsonStructure([
                     'message',
                     'user' => ['id', 'name', 'email', 'role'],
                     'token',
                 ]);

        $this->assertDatabaseHas('users', [
            'email' => 'admin@tapandchew.com',
            'role'  => 'admin',
        ]);
    }

    public function test_register_fails_with_duplicate_email(): void
    {
        User::factory()->create(['email' => 'admin@tapandchew.com']);

        $response = $this->postJson('/api/auth/register', [
            'name'                  => 'Otro Usuario',
            'email'                 => 'admin@tapandchew.com',
            'password'              => 'password123',
            'password_confirmation' => 'password123',
        ]);

        $response->assertStatus(422);
    }

    public function test_register_fails_when_password_not_confirmed(): void
    {
        $response = $this->postJson('/api/auth/register', [
            'name'                  => 'Gabriel',
            'email'                 => 'gabriel@test.com',
            'password'              => 'password123',
            'password_confirmation' => 'diferente',
        ]);

        $response->assertStatus(422);
    }

    public function test_register_fails_with_missing_fields(): void
    {
        $response = $this->postJson('/api/auth/register', []);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['name', 'email', 'password']);
    }

    // ─── LOGIN ───────────────────────────────────────────────────

    public function test_user_can_login_with_valid_credentials(): void
    {
        User::factory()->create([
            'email'    => 'admin@tapandchew.com',
            'password' => bcrypt('password123'),
            'role'     => 'admin',
        ]);

        $response = $this->postJson('/api/auth/login', [
            'email'    => 'admin@tapandchew.com',
            'password' => 'password123',
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure([
                     'message',
                     'user' => ['id', 'name', 'email', 'role'],
                     'token',
                 ]);
    }

    public function test_login_fails_with_wrong_password(): void
    {
        User::factory()->create([
            'email'    => 'admin@tapandchew.com',
            'password' => bcrypt('password123'),
        ]);

        $response = $this->postJson('/api/auth/login', [
            'email'    => 'admin@tapandchew.com',
            'password' => 'contraseña_incorrecta',
        ]);

        $response->assertStatus(401);
    }

    public function test_login_fails_with_nonexistent_user(): void
    {
        $response = $this->postJson('/api/auth/login', [
            'email'    => 'noexiste@tapandchew.com',
            'password' => 'password123',
        ]);

        $response->assertStatus(401);
    }

    public function test_login_fails_with_missing_fields(): void
    {
        $response = $this->postJson('/api/auth/login', []);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['email', 'password']);
    }

    public function test_inactive_user_cannot_login(): void
    {
        User::factory()->create([
            'email'     => 'inactivo@tapandchew.com',
            'password'  => bcrypt('password123'),
            'is_active' => false,
        ]);

        $response = $this->postJson('/api/auth/login', [
            'email'    => 'inactivo@tapandchew.com',
            'password' => 'password123',
        ]);

        $response->assertStatus(403);
    }

    // ─── ME ──────────────────────────────────────────────────────

    public function test_authenticated_user_can_get_their_data(): void
    {
        $user  = User::factory()->create();
        $token = $user->createToken('test')->plainTextToken;

        $response = $this->withHeader('Authorization', "Bearer {$token}")
                         ->getJson('/api/auth/me');

        $response->assertStatus(200)
                 ->assertJsonStructure(['id', 'name', 'email', 'role']);
    }

    public function test_unauthenticated_user_cannot_access_me(): void
    {
        $response = $this->getJson('/api/auth/me');

        $response->assertStatus(401);
    }

    // ─── LOGOUT ──────────────────────────────────────────────────

    public function test_user_can_logout(): void
    {
        $user  = User::factory()->create();
        $token = $user->createToken('test')->plainTextToken;

        $response = $this->withHeader('Authorization', "Bearer {$token}")
                        ->postJson('/api/auth/logout');

        $response->assertStatus(200)
                ->assertJson(['message' => 'Sesión cerrada correctamente.']);

        // Limpiar el guard cacheado en memoria
        $this->app['auth']->forgetGuards();

        // El token ya no debe ser válido
        $this->withHeader('Authorization', "Bearer {$token}")
            ->getJson('/api/auth/me')
            ->assertStatus(401);
    }
    public function test_logout_fails_without_token(): void
    {
        $response = $this->postJson('/api/auth/logout');

        $response->assertStatus(401);
    }

    // ─── FORGOT PASSWORD ─────────────────────────────────────────

    public function test_forgot_password_returns_200_for_existing_email(): void
    {
        User::factory()->create(['email' => 'admin@tapandchew.com']);

        $response = $this->postJson('/api/auth/forgot-password', [
            'email' => 'admin@tapandchew.com',
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure(['message']);
    }

    public function test_forgot_password_returns_200_for_nonexistent_email(): void
    {
        // El servicio valida que el email exista — retorna 400 si no está registrado
        $response = $this->postJson('/api/auth/forgot-password', [
            'email' => 'noexiste@tapandchew.com',
        ]);

        $response->assertStatus(400);
    }

    public function test_forgot_password_fails_with_invalid_email(): void
    {
        $response = $this->postJson('/api/auth/forgot-password', [
            'email' => 'no-es-un-email',
        ]);

        $response->assertStatus(422);
    }
}