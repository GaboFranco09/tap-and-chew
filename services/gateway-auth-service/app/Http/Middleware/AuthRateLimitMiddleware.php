<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

class AuthRateLimitMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        $key = 'auth:' . $request->ip();

        if (RateLimiter::tooManyAttempts($key, 10)) {
            $seconds = RateLimiter::availableIn($key);
            return response()->json([
                'message' => "Demasiados intentos. Intenta de nuevo en {$seconds} segundos.",
            ], 429);
        }

        RateLimiter::hit($key, 900); // 15 minutos

        return $next($request);
    }
}