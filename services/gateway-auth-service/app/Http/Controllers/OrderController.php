<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class OrderController extends Controller
{
    private string $baseUrl;
    private array  $internalHeaders;

    public function __construct()
    {
        $this->baseUrl = config('services.order.url');
        $this->internalHeaders = [
            'X-Internal-Secret' => env('INTERNAL_SECRET'),
            'Accept'            => 'application/json',
            'Content-Type'      => 'application/json',
        ];
    }

    // GET /api/orders
    public function getOrders(Request $request)
    {
        try {
            $query    = $request->getQueryString();
            $url      = "{$this->baseUrl}/api/orders" . ($query ? "?{$query}" : '');
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)->get($url);

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Order Service no disponible.'], 503);
        }
    }

    // POST /api/orders
    public function createOrder(Request $request)
    {
        $request->validate([
            'kiosk_id' => 'required|string',
            'items'    => 'required|array|min:1',
            'total'    => 'required|numeric|min:0',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/orders", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Order Service no disponible.'], 503);
        }
    }

    // GET /api/orders/{id}
    public function getOrder(string $id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/orders/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Order Service no disponible.'], 503);
        }
    }

    // PATCH /api/orders/{id}/status
    public function updateStatus(Request $request, string $id)
    {
        $request->validate([
            'status' => 'required|in:pending,confirmed,preparing,ready,delivered,cancelled',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->patch("{$this->baseUrl}/api/orders/{$id}/status", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Order Service no disponible.'], 503);
        }
    }

    // DELETE /api/orders/{id}
    public function cancelOrder(string $id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->delete("{$this->baseUrl}/api/orders/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Order Service no disponible.'], 503);
        }
    }
}