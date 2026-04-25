<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PaymentController extends Controller
{
    private string $baseUrl;
    private array  $internalHeaders;

    public function __construct()
    {
        $this->baseUrl = config('services.payment.url');
        $this->internalHeaders = [
            'X-Internal-Secret' => env('INTERNAL_SECRET'),
            'Accept'            => 'application/json',
            'Content-Type'      => 'application/json',
        ];
    }

    // GET /api/payments
    public function getPayments(Request $request)
    {
        try {
            $query    = $request->getQueryString();
            $url      = "{$this->baseUrl}/api/payments" . ($query ? "?{$query}" : '');
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)->get($url);

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Payment Service no disponible.'], 503);
        }
    }

    // GET /api/payments/stats
    public function getStats()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/payments/stats");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Payment Service no disponible.'], 503);
        }
    }

    // POST /api/payments
    public function createPayment(Request $request)
    {
        $request->validate([
            'order_id'       => 'required|string',
            'kiosk_id'       => 'required|string',
            'items'          => 'required|array|min:1',
            'subtotal'       => 'required|numeric',
            'total'          => 'required|numeric',
            'payment_method' => 'required|in:cash,card,qr',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/payments", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Payment Service no disponible.'], 503);
        }
    }

    // PATCH /api/payments/{id}/refund
    public function refund(string $id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->patch("{$this->baseUrl}/api/payments/{$id}/refund");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Payment Service no disponible.'], 503);
        }
    }
}