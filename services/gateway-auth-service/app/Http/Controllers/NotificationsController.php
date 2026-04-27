<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class NotificationsController extends Controller
{
    private string $baseUrl;
    private array  $internalHeaders;

    public function __construct()
    {
        $this->baseUrl = config('services.notifications.url');
        $this->internalHeaders = [
            'X-Internal-Secret' => env('INTERNAL_SECRET'),
            'Accept'            => 'application/json',
            'Content-Type'      => 'application/json',
        ];
    }

    // GET /api/notifications/order/{order_id}
    public function getByOrder(string $order_id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/notifications/order/{$order_id}");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Notifications Service no disponible.'], 503);
        }
    }

    // POST /api/notifications
    public function create(Request $request)
    {
        $request->validate([
            'order_id' => 'required|string',
            'type'     => 'required|in:order_confirmed,order_ready,payment_processed',
            'message'  => 'required|string',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/notifications", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Notifications Service no disponible.'], 503);
        }
    }

    // PATCH /api/notifications/{id}/read
    public function markAsRead(string $id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->patch("{$this->baseUrl}/api/notifications/{$id}/read");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Notifications Service no disponible.'], 503);
        }
    }
}