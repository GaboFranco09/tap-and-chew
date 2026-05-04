<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\MenuController;
use App\Http\Controllers\OrderController;
use App\Http\Controllers\KitchenController;
use App\Http\Controllers\PaymentController;
use App\Http\Controllers\NotificationsController;
use Illuminate\Support\Facades\Route;

// ─── HEALTH ──────────────────────────────────────────────────────
Route::get('/health', fn() => response()->json([
    'status'  => 'ok',
    'service' => 'gateway-auth-service',
    'port'    => 8000,
]));

// ─── AUTH PÚBLICO ────────────────────────────────────────────────
Route::prefix('auth')->middleware('auth.ratelimit')->group(function () {
    Route::post('/register',        [AuthController::class, 'register']);
    Route::post('/login',           [AuthController::class, 'login']);
    Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
    Route::post('/reset-password',  [AuthController::class, 'resetPassword']);
});

// ─── RUTAS PROTEGIDAS ────────────────────────────────────────────
Route::middleware('jwt.auth')->group(function () {

    // Auth
    Route::prefix('auth')->group(function () {
        Route::post('/logout', [AuthController::class, 'logout']);
        Route::get('/me',      [AuthController::class, 'me']);
    });

    // Menu Service
    Route::prefix('menu')->group(function () {
        Route::get('/categories',        [MenuController::class, 'getCategories']);
        Route::get('/categories/active', [MenuController::class, 'getActiveCategories']);
        Route::post('/categories',       [MenuController::class, 'createCategory']);
        Route::get('/products',          [MenuController::class, 'getProducts']);
        Route::get('/products/available',[MenuController::class, 'getAvailableProducts']);
        Route::post('/products',         [MenuController::class, 'createProduct']);
        Route::get('/combos',            [MenuController::class, 'getCombos']);
        Route::get('/combos/active',     [MenuController::class, 'getActiveCombos']);
    });

    // Order Service
    Route::prefix('orders')->group(function () {
        Route::get('/',              [OrderController::class, 'getOrders']);
        Route::post('/',             [OrderController::class, 'createOrder']);
        Route::get('/{id}',          [OrderController::class, 'getOrder']);
        Route::patch('/{id}/status', [OrderController::class, 'updateStatus']);
        Route::delete('/{id}',       [OrderController::class, 'cancelOrder']);
    });

    // Kitchen Service
    Route::prefix('kitchen')->group(function () {
        Route::post('/sync',                              [KitchenController::class, 'sync']);
        Route::get('/queue',                              [KitchenController::class, 'getQueue']);
        Route::get('/history',                            [KitchenController::class, 'getHistory']);
        Route::post('/orders',                            [KitchenController::class, 'receiveOrder']);
        Route::patch('/orders/{order_id}/start',          [KitchenController::class, 'startOrder']);
        Route::patch('/orders/{order_id}/complete',       [KitchenController::class, 'completeOrder']);
        Route::patch('/orders/{order_id}/items/{item_id}/toggle', [KitchenController::class, 'toggleItem']);
    });

    // Payment Service
    Route::prefix('payments')->group(function () {
        Route::get('/',          [PaymentController::class, 'getPayments']);
        Route::get('/stats',     [PaymentController::class, 'getStats']);
        Route::post('/',         [PaymentController::class, 'createPayment']);
        Route::patch('/{id}/refund', [PaymentController::class, 'refund']);
    });

    // Notifications Service
    Route::prefix('notifications')->group(function () {
        Route::get('/order/{order_id}', [NotificationsController::class, 'getByOrder']);
        Route::post('/',                [NotificationsController::class, 'create']);
        Route::patch('/{id}/read',      [NotificationsController::class, 'markAsRead']);
    });
});